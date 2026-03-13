
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk

st.set_page_config(page_title="Yalla CXO", page_icon="🧭", layout="wide")

@st.cache_data
def load_data():
    preferred = "Fractional-CXO-Dubai-Top-100-Framework-enhanced.csv"
    fallback = "fractional_cxo_dubai_top100_framework_ready.csv"
    try:
        return pd.read_csv(preferred)
    except Exception:
        return pd.read_csv(fallback)


def aed(x):
    x = float(x)
    if abs(x) >= 1_000_000_000:
        return f"AED {x/1_000_000_000:.2f}B"
    if abs(x) >= 1_000_000:
        return f"AED {x/1_000_000:.2f}M"
    if abs(x) >= 1_000:
        return f"AED {x/1_000:.1f}K"
    return f"AED {x:,.0f}"


def safe_series(df, col, default=0.0):
    if col not in df.columns:
        return pd.Series([default] * len(df), index=df.index)
    return df[col]


def safe_value(row, col, default=0.0):
    return row[col] if col in row.index and pd.notna(row[col]) else default


def apply_style():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
        .stApp {background: #F7F9FC; color: #111827;}
        [data-testid="stSidebar"] {display:none;}
        .block-container {padding-top: 1rem; max-width: 1500px;}
        .topbar {background:white; border:1px solid #E5E7EB; border-radius:20px; padding:1rem 1.15rem; margin-bottom:0.8rem;}
        .appname {font-size:2rem; font-weight:800; color:#111827; margin:0;}
        .subcopy {color:#6B7280; margin:0.35rem 0 0 0; line-height:1.5;}
        .companyhero {background:linear-gradient(135deg,#0F172A 0%,#1D4ED8 55%,#14B8A6 100%); color:white; border-radius:24px; padding:1.1rem 1.15rem; margin-bottom:0.9rem;}
        .companyhero h2 {margin:0; font-size:1.7rem; color:white;}
        .companyhero p {margin:0.4rem 0 0 0; color:rgba(255,255,255,0.88); line-height:1.55;}
        .chiprow {display:flex; flex-wrap:wrap; gap:0.45rem; margin-top:0.8rem;}
        .chip {display:inline-flex; padding:0.42rem 0.7rem; border-radius:999px; background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.16); font-size:0.8rem;}
        .metricbox {background:white; border:1px solid #E5E7EB; border-radius:18px; padding:0.9rem 0.95rem; min-height:115px;}
        .metriclabel {font-size:0.74rem; text-transform:uppercase; letter-spacing:0.08em; color:#6B7280; margin-bottom:0.28rem;}
        .metricvalue {font-size:1.42rem; font-weight:800; color:#111827; line-height:1.1; margin-bottom:0.2rem;}
        .metricsub {font-size:0.85rem; color:#6B7280; line-height:1.42;}
        .panel {background:white; border:1px solid #E5E7EB; border-radius:20px; padding:1rem 1rem; margin-bottom:0.9rem;}
        .sectiontitle {font-size:1.1rem; font-weight:800; color:#111827; margin:0 0 0.1rem 0;}
        .sectioncopy {font-size:0.92rem; color:#6B7280; margin:0 0 0.85rem 0; line-height:1.5;}
        .stTabs [data-baseweb="tab-list"] {gap:0.4rem; margin-bottom:0.6rem; flex-wrap:wrap;}
        .stTabs [data-baseweb="tab"] {background:white; border:1px solid #E5E7EB; border-radius:12px; padding:0.55rem 0.85rem;}
        .stTabs [aria-selected="true"] {background:#EFF6FF; border-color:#2563EB; color:#111827;}
        div[data-testid="stDataFrame"] {border:1px solid #E5E7EB; border-radius:16px; overflow:hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def chart_theme():
    return {
        "config": {
            "background": "transparent",
            "view": {"stroke": None},
            "title": {"anchor": "start", "font": "Inter", "fontSize": 18, "fontWeight": 700, "color": "#111827"},
            "axis": {"labelColor": "#6B7280", "titleColor": "#111827", "gridColor": "#E5E7EB", "labelFont": "Inter", "titleFont": "Inter"},
            "legend": {"labelColor": "#6B7280", "titleColor": "#111827", "labelFont": "Inter", "titleFont": "Inter"},
        }
    }

try:
    alt.themes.register("yalla_cxo_clean", chart_theme)
except Exception:
    pass
alt.themes.enable("yalla_cxo_clean")

ROLE_COLS = {
    "CFO": "cfo_need_score",
    "CTO": "cto_need_score",
    "CHRO": "chro_need_score",
    "CMO": "cmo_need_score",
    "COO": "coo_need_score",
}

ARCHETYPE_MAP = {
    "CFO": "Finance-stressed",
    "CTO": "Tech-transformation",
    "CHRO": "People-scaling",
    "CMO": "Marketing-efficiency",
    "COO": "Operational-efficiency",
}


def role_order(row):
    scores = {role: float(safe_value(row, col, 0.0)) for role, col in ROLE_COLS.items()}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def derive_fields(df):
    out = df.copy()
    primary_roles, secondary_roles, primary_scores, secondary_scores = [], [], [], []
    for _, row in out.iterrows():
        ordered = role_order(row)
        primary_roles.append(ordered[0][0])
        secondary_roles.append(ordered[1][0])
        primary_scores.append(float(ordered[0][1]))
        secondary_scores.append(float(ordered[1][1]))
    out["primary_role_derived"] = primary_roles
    out["secondary_role_derived"] = secondary_roles
    out["primary_role_score"] = primary_scores
    out["secondary_role_score"] = secondary_scores
    out["need_archetype_derived"] = out["primary_role_derived"].map(ARCHETYPE_MAP)
    out["win_pct"] = safe_series(out, "win_probability") * 100
    out["response_pct"] = safe_series(out, "response_probability") * 100
    out["weighted_acv"] = safe_series(out, "expected_annual_contract_value_aed") * safe_series(out, "win_probability")
    out["weighted_ltv"] = safe_series(out, "expected_account_ltv_aed") * safe_series(out, "win_probability")
    out["cost_gap_vs_full_time"] = safe_series(out, "full_time_equivalent_cost_aed") - safe_series(out, "fractional_ai_solution_cost_aed")
    out["value_at_risk"] = safe_series(out, "expected_account_ltv_aed") * safe_series(out, "client_churn_risk_score") / 100.0
    out["priority_index"] = (
        0.28 * out["primary_role_score"] + 0.22 * safe_series(out, "urgency_score") + 0.20 * out["win_pct"] +
        0.15 * out["response_pct"] + 0.15 * safe_series(out, "account_health_score")
    )
    out["priority_band"] = pd.qcut(out["priority_index"].rank(method="first"), 4, labels=["Watch", "Build", "Prioritize", "Act now"])
    out["close_month"] = np.clip(np.ceil(safe_series(out, "expected_close_days") / 30), 1, 6).astype(int)
    out["close_month_label"] = "M" + out["close_month"].astype(str)
    out["close_bucket"] = pd.cut(safe_series(out, "expected_close_days"), bins=[-1, 30, 60, 90, 9999], labels=["0-30d", "31-60d", "61-90d", "90d+"])
    return out


def metric_card(label, value, sub):
    st.markdown(f"<div class='metricbox'><div class='metriclabel'>{label}</div><div class='metricvalue'>{value}</div><div class='metricsub'>{sub}</div></div>", unsafe_allow_html=True)


def section_open(title, copy):
    st.markdown(f"<div class='panel'><div class='sectiontitle'>{title}</div><div class='sectioncopy'>{copy}</div>", unsafe_allow_html=True)


def section_close():
    st.markdown("</div>", unsafe_allow_html=True)


def company_selector(df):
    c1, c2, c3, c4 = st.columns([1.8, 1.1, 1.1, 1.2], gap="medium")
    with c2:
        sector_options = ["All"] + sorted(df["sector"].dropna().unique().tolist())
        sector = st.selectbox("Sector filter", sector_options, index=0, key="sector_filter_main")
    with c3:
        role_options = ["All"] + list(ROLE_COLS.keys())
        role = st.selectbox("Primary role filter", role_options, index=0, key="role_filter_main")
    with c4:
        min_win = st.slider("Min win probability", 0.0, 1.0, 0.0, 0.01, key="min_win_main")

    filtered = df.copy()
    if sector != "All":
        filtered = filtered[filtered["sector"] == sector]
    if role != "All":
        filtered = filtered[filtered["primary_role_derived"] == role]
    filtered = filtered[filtered["win_probability"] >= min_win].copy()
    if filtered.empty:
        return None, None

    companies = sorted(filtered["company_name"].tolist())
    current = st.session_state.get("selected_company_main")
    default_index = companies.index(current) if current in companies else 0
    with c1:
        selected = st.selectbox("Selected company", companies, index=default_index, key="selected_company_main")

    row = filtered.loc[filtered["company_name"] == selected].iloc[0]
    return filtered, row


def hero(row):
    chips = "".join([
        f"<div class='chip'>Sector · {row['sector']}</div>",
        f"<div class='chip'>Primary · {row['primary_role_derived']}</div>",
        f"<div class='chip'>Secondary · {row['secondary_role_derived']}</div>",
        f"<div class='chip'>Priority · {row['priority_band']}</div>",
        f"<div class='chip'>Zone · {safe_value(row, 'hq_zone', 'Dubai')}</div>",
    ])
    context = safe_value(row, 'company_context_line', 'Dubai corporate with meaningful executive demand and measurable value-creation potential.')
    st.markdown(
        f"""
        <div class='companyhero'>
            <h2>{row['company_name']}</h2>
            <p>{context}</p>
            <div class='chiprow'>{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def overview_rank(filtered):
    df = filtered[["company_name", "priority_index", "weighted_acv", "primary_role_derived"]].sort_values("priority_index", ascending=False).head(12)
    return alt.Chart(df).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X("priority_index:Q", title="Priority index"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color("primary_role_derived:N", title="Primary role"),
        tooltip=["company_name", "primary_role_derived", alt.Tooltip("priority_index:Q", format=".1f"), alt.Tooltip("weighted_acv:Q", format=",.0f")],
    ).properties(title="Top prioritized accounts", height=340)


def overview_scatter(filtered, row):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    base = alt.Chart(df).mark_circle(opacity=0.8, stroke="white", strokeWidth=0.6).encode(
        x=alt.X("urgency_score:Q", title="Urgency score"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV"),
        size=alt.Size("estimated_annual_savings_aed:Q", scale=alt.Scale(range=[80, 1300]), title="Savings"),
        color=alt.condition(alt.datum.selected, alt.value("#DC2626"), alt.Color("primary_role_derived:N", title="Primary role")),
        tooltip=["company_name", "sector", "primary_role_derived", alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    label = alt.Chart(df[df["selected"]]).mark_text(dx=8, dy=-8).encode(x="urgency_score:Q", y="weighted_acv:Q", text="company_name:N")
    return (base + label).properties(title="Urgency vs value map", height=340)


def role_profile(row):
    df = pd.DataFrame({"Role": list(ROLE_COLS.keys()), "Need": [float(safe_value(row, ROLE_COLS[r], 0)) for r in ROLE_COLS]}).sort_values("Need", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X("Need:Q", title="Need score", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Role:N", sort=None, title=""),
        color=alt.Color("Role:N", legend=None),
        tooltip=["Role", alt.Tooltip("Need:Q", format=".1f")],
    )
    text = alt.Chart(df).mark_text(dx=8, align="left").encode(x="Need:Q", y=alt.Y("Role:N", sort=None), text=alt.Text("Need:Q", format=".1f"))
    return (bars + text).properties(title="Role-demand profile", height=300)


def value_stack(row):
    df = pd.DataFrame([
        ["Expected ACV", float(safe_value(row, "expected_annual_contract_value_aed", 0))],
        ["Weighted ACV", float(safe_value(row, "weighted_acv", 0))],
        ["Weighted LTV", float(safe_value(row, "weighted_ltv", 0))],
        ["Savings", float(safe_value(row, "estimated_annual_savings_aed", 0))],
    ], columns=["Metric", "Value"])
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("Metric:N", title=""),
        y=alt.Y("Value:Q", title="AED"),
        color=alt.Color("Metric:N", legend=None),
        tooltip=["Metric", alt.Tooltip("Value:Q", format=",.0f")],
    ).properties(title="Value profile", height=300)


def portfolio_heatmap(filtered):
    df = filtered.groupby(["sector", "primary_role_derived"], as_index=False).size().rename(columns={"size": "accounts"})
    heat = alt.Chart(df).mark_rect().encode(
        x=alt.X("primary_role_derived:N", title="Primary role"),
        y=alt.Y("sector:N", title="Sector"),
        color=alt.Color("accounts:Q", scale=alt.Scale(scheme="blues"), title="Accounts"),
        tooltip=["sector", "primary_role_derived", "accounts"],
    )
    text = alt.Chart(df).mark_text(fontSize=11).encode(
        x="primary_role_derived:N", y="sector:N", text="accounts:Q",
        color=alt.condition(alt.datum.accounts >= 2, alt.value("white"), alt.value("#111827")),
    )
    return (heat + text).properties(title="Sector x role demand", height=320)


def map_view(filtered):
    if "latitude" not in filtered.columns or "longitude" not in filtered.columns:
        st.info("No map columns found.")
        return

    m = filtered[["company_name", "latitude", "longitude", "weighted_acv", "primary_role_derived", "hq_zone"]].dropna().copy()
    if m.empty:
        st.info("No map-ready rows available.")
        return

    m["latitude"] = pd.to_numeric(m["latitude"], errors="coerce")
    m["longitude"] = pd.to_numeric(m["longitude"], errors="coerce")
    m["weighted_acv"] = pd.to_numeric(m["weighted_acv"], errors="coerce").fillna(0)
    m = m.dropna(subset=["latitude", "longitude"])
    if m.empty:
        st.info("Map coordinates are invalid after cleaning.")
        return

    max_val = max(float(m["weighted_acv"].max()), 1.0)
    m["radius"] = ((m["weighted_acv"] / max_val) * 6000 + 250).clip(250, 2200)

    st.caption("Smaller circles and a flat map view make the Dubai clusters readable.")

    deck = pdk.Deck(
        map_style="light",
        initial_view_state=pdk.ViewState(
            latitude=float(m["latitude"].mean()),
            longitude=float(m["longitude"].mean()),
            zoom=10.4,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=m,
                get_position='[longitude, latitude]',
                get_radius='radius',
                radius_units='meters',
                radius_min_pixels=4,
                radius_max_pixels=18,
                get_fill_color='[37, 99, 235, 140]',
                get_line_color='[255,255,255,180]',
                line_width_min_pixels=1,
                pickable=True,
                stroked=True,
            )
        ],
        tooltip={
            "html": "<b>{company_name}</b><br/>Zone: {hq_zone}<br/>Primary role: {primary_role_derived}<br/>Weighted ACV: {weighted_acv}",
            "style": {"backgroundColor": "#111827", "color": "white"},
        },
    )
    st.pydeck_chart(deck, use_container_width=True)


def pipeline_chart(filtered):
    df = filtered.groupby("close_month_label", as_index=False).agg(weighted_acv=("weighted_acv", "sum"))
    order = pd.DataFrame({"close_month_label": ["M1", "M2", "M3", "M4", "M5", "M6"]})
    df = order.merge(df, on="close_month_label", how="left").fillna(0)
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color="#2563EB").encode(
        x=alt.X("close_month_label:N", title="Expected close month"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV"),
        tooltip=["close_month_label", alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color="#14B8A6").encode(x="close_month_label:N", y="weighted_acv:Q")
    return (bars + line).properties(title="Weighted pipeline by month", height=320)


def funnel(row):
    touches = max(int(safe_value(row, "sales_touchpoints_90d", 0)), 1)
    responses = max(int(round(touches * float(safe_value(row, "response_probability", 0)) * 0.9)), 1)
    meetings = max(int(safe_value(row, "meetings_booked_90d", 0)), 1 if responses > 1 else 0)
    proposals = max(int(safe_value(row, "proposal_count_90d", 0)), 1 if meetings > 1 else 0)
    closes = max(float(safe_value(row, "win_probability", 0)) * max(1, proposals), 0.5)
    df = pd.DataFrame([["Touches", touches], ["Responses", responses], ["Meetings", meetings], ["Proposals", proposals], ["Expected closes", closes]], columns=["Stage", "Value"])
    return alt.Chart(df).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X("Value:Q", title="Volume / expected outcome"),
        y=alt.Y("Stage:N", sort="-x", title=""),
        color=alt.Color("Stage:N", legend=None),
        tooltip=["Stage", alt.Tooltip("Value:Q", format=".1f")],
    ).properties(title="Commercial funnel", height=300)


def comparables(filtered, row):
    df = filtered.copy()
    df["distance"] = (
        (df["revenue_aed_bn"] - row["revenue_aed_bn"]).abs() * 2 +
        (df["urgency_score"] - row["urgency_score"]).abs() * 0.45 +
        (df["expected_annual_contract_value_aed"] - row["expected_annual_contract_value_aed"]).abs() / 500000
    )
    out = df[df["company_name"] != row["company_name"]].sort_values("distance").head(8)[[
        "company_name", "sector", "primary_role_derived", "secondary_role_derived", "weighted_acv", "estimated_annual_savings_aed"
    ]].copy()
    out["weighted_acv"] = out["weighted_acv"].map(aed)
    out["estimated_annual_savings_aed"] = out["estimated_annual_savings_aed"].map(aed)
    return out.rename(columns={
        "company_name": "Comparable company",
        "primary_role_derived": "Primary role",
        "secondary_role_derived": "Secondary role",
        "weighted_acv": "Weighted ACV",
        "estimated_annual_savings_aed": "Savings",
    })


def main():
    apply_style()
    st.markdown("<div class='topbar'><div class='appname'>Yalla CXO</div><p class='subcopy'>A Dubai-focused lead prioritization and service-design dashboard for large corporates, built around fractional CXO demand, savings logic, and portfolio decision support.</p></div>", unsafe_allow_html=True)
    df = derive_fields(load_data())
    filtered, row = company_selector(df)
    if filtered is None or row is None:
        st.warning("No companies match the current main-screen filters.")
        st.stop()

    hero(row)

    m1, m2, m3, m4, m5, m6 = st.columns(6, gap="medium")
    with m1:
        metric_card("Primary role", row["primary_role_derived"], f"Need score {row['primary_role_score']:.1f}")
    with m2:
        metric_card("Secondary role", row["secondary_role_derived"], f"Need score {row['secondary_role_score']:.1f}")
    with m3:
        metric_card("Expected ACV", aed(row["expected_annual_contract_value_aed"]), "Headline annual contract value")
    with m4:
        metric_card("Weighted ACV", aed(row["weighted_acv"]), "Adjusted by win probability")
    with m5:
        metric_card("Savings", aed(row["estimated_annual_savings_aed"]), "Versus full-time executive cost")
    with m6:
        metric_card("Priority index", f"{row['priority_index']:.1f}", f"Band: {row['priority_band']}")

    t1, t2, t3, t4, t5 = st.tabs(["Overview", "Portfolio", "Service Design", "Pipeline", "Map"])

    with t1:
        section_open("Executive overview", "Start with the selected company, then compare it against the strongest opportunities in the current filtered portfolio.")
        a, b = st.columns([0.52, 0.48], gap="large")
        with a:
            st.altair_chart(role_profile(row), use_container_width=True)
        with b:
            st.altair_chart(value_stack(row), use_container_width=True)
        c, d = st.columns([0.54, 0.46], gap="large")
        with c:
            st.altair_chart(overview_rank(filtered), use_container_width=True)
        with d:
            st.dataframe(comparables(filtered, row), use_container_width=True, hide_index=True, height=340)
        section_close()

    with t2:
        section_open("Portfolio view", "See where the selected company sits relative to the rest of the book by urgency, value, sector, and role demand.")
        a, b = st.columns([0.55, 0.45], gap="large")
        with a:
            st.altair_chart(overview_scatter(filtered, row), use_container_width=True)
        with b:
            st.altair_chart(portfolio_heatmap(filtered), use_container_width=True)
        section_close()

    with t3:
        section_open("Service design studio", "Translate the account into a practical recommendation: lead role, expansion role, AI layer, and delivery logic.")
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            st.info(f"**Lead with {row['primary_role_derived']}**\n\nThis is the highest-scoring executive need and should anchor the opening offer.")
        with c2:
            st.info(f"**Expand into {row['secondary_role_derived']}**\n\nThis is the strongest adjacent role once the first intervention proves value.")
        with c3:
            st.info(f"**Use AI-supported delivery**\n\nSupport the offer with {safe_value(row, 'ai_supported_roles', 'AI-enabled support roles')} to improve scalability and cost efficiency.")
        st.dataframe(pd.DataFrame({
            "Field": ["Archetype", "Delivery model", "Location zone", "Location context", "Service package", "Next action"],
            "Value": [
                row['need_archetype_derived'],
                np.where(row['secondary_role_score'] >= 70, 'Primary CXO + cross-functional expansion', 'Primary CXO + AI-enabled support'),
                safe_value(row, 'hq_zone', 'Dubai'),
                safe_value(row, 'hq_zone_context', 'Corporate location within Dubai'),
                safe_value(row, 'recommended_service_package', 'Recommended package not specified'),
                safe_value(row, 'ideal_next_action', 'Prioritize executive discovery and quantify value pool'),
            ]
        }), use_container_width=True, hide_index=True)
        section_close()

    with t4:
        section_open("Pipeline planning", "Use the filtered opportunity set for light-weight planning: value timing, account motion, and commercial funnel strength.")
        a, b = st.columns([0.5, 0.5], gap="large")
        with a:
            st.altair_chart(pipeline_chart(filtered), use_container_width=True)
        with b:
            st.altair_chart(funnel(row), use_container_width=True)
        section_close()

    with t5:
        section_open("Dubai map", "The dataset has been enriched with synthetic Dubai zone, city, country, and latitude/longitude fields so the portfolio can be viewed geographically.")
        map_view(filtered)
        section_close()

    st.download_button(
        "Download enhanced filtered dataset",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="yalla_cxo_filtered_enhanced.csv",
        mime="text/csv",
        use_container_width=True,
    )

if __name__ == "__main__":
    main()
