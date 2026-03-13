
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Dubai CXO Control Tower",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


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
    return row[col] if col in row.index else default


def theme_chart():
    return {
        "config": {
            "background": "transparent",
            "view": {"stroke": None},
            "axis": {
                "labelColor": "#4B5563",
                "titleColor": "#111827",
                "gridColor": "#E5E7EB",
                "labelFont": "Inter",
                "titleFont": "Inter",
            },
            "legend": {
                "labelColor": "#4B5563",
                "titleColor": "#111827",
                "labelFont": "Inter",
                "titleFont": "Inter",
            },
            "title": {
                "color": "#111827",
                "font": "Inter",
                "fontSize": 18,
                "fontWeight": 700,
                "anchor": "start",
            },
        }
    }


try:
    alt.themes.register("clean_consulting", theme_chart)
except Exception:
    pass
alt.themes.enable("clean_consulting")


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

PALETTE = ["#2563EB", "#14B8A6", "#7C3AED", "#F59E0B", "#EF4444", "#0EA5E9"]


def role_order(row):
    scores = {role: float(safe_value(row, col, 0.0)) for role, col in ROLE_COLS.items()}
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ordered


def derive_fields(df):
    out = df.copy()

    primary_roles = []
    secondary_roles = []
    primary_scores = []
    secondary_scores = []
    recommendation_text = []

    for _, row in out.iterrows():
        ordered = role_order(row)
        primary_roles.append(ordered[0][0])
        secondary_roles.append(ordered[1][0])
        primary_scores.append(float(ordered[0][1]))
        secondary_scores.append(float(ordered[1][1]))
        recommendation_text.append(f"{ordered[0][0]} led offer + {ordered[1][0]} expansion")

    out["primary_role_derived"] = primary_roles
    out["secondary_role_derived"] = secondary_roles
    out["primary_role_score"] = primary_scores
    out["secondary_role_score"] = secondary_scores
    out["need_archetype_derived"] = out["primary_role_derived"].map(ARCHETYPE_MAP)
    out["recommendation_logic"] = recommendation_text

    out["win_pct"] = safe_series(out, "win_probability") * 100
    out["response_pct"] = safe_series(out, "response_probability") * 100
    out["weighted_acv"] = safe_series(out, "expected_annual_contract_value_aed") * safe_series(out, "win_probability")
    out["weighted_ltv"] = safe_series(out, "expected_account_ltv_aed") * safe_series(out, "win_probability")
    out["cost_gap_vs_full_time"] = safe_series(out, "full_time_equivalent_cost_aed") - safe_series(out, "fractional_ai_solution_cost_aed")
    out["value_at_risk"] = safe_series(out, "expected_account_ltv_aed") * safe_series(out, "client_churn_risk_score") / 100.0
    out["roi_proxy"] = safe_series(out, "estimated_annual_savings_aed") / safe_series(out, "fractional_ai_solution_cost_aed").replace(0, np.nan)
    out["roi_proxy"] = out["roi_proxy"].replace([np.inf, -np.inf], np.nan).fillna(0)

    out["north_star_value"] = (
        0.35 * out["weighted_acv"]
        + 0.20 * safe_series(out, "estimated_annual_savings_aed")
        + 0.15 * out["weighted_ltv"]
        + 0.15 * safe_series(out, "urgency_score") * 10000
        + 0.15 * out["response_pct"] * 10000
    )

    out["priority_index"] = (
        0.28 * out["primary_role_score"]
        + 0.22 * safe_series(out, "urgency_score")
        + 0.20 * out["win_pct"]
        + 0.15 * out["response_pct"]
        + 0.15 * safe_series(out, "account_health_score")
    )

    out["priority_band"] = pd.qcut(
        out["priority_index"].rank(method="first"),
        4,
        labels=["Watch", "Build", "Prioritize", "Act now"],
    )

    out["value_band"] = pd.qcut(
        safe_series(out, "expected_account_ltv_aed").rank(method="first"),
        4,
        labels=["Low", "Mid", "High", "Elite"],
    )

    out["close_bucket"] = pd.cut(
        safe_series(out, "expected_close_days"),
        bins=[-1, 30, 60, 90, 9999],
        labels=["0-30d", "31-60d", "61-90d", "90d+"],
    )

    out["close_month"] = np.clip(np.ceil(safe_series(out, "expected_close_days") / 30), 1, 6).astype(int)
    out["close_month_label"] = "M" + out["close_month"].astype(str)

    out["delivery_model"] = np.where(
        out["secondary_role_score"] >= 70,
        "Primary CXO + cross-functional expansion",
        "Primary CXO + AI-enabled support",
    )

    return out


def filter_data(df):
    sidebar = st.sidebar
    sidebar.header("Controls")

    sectors = sidebar.multiselect(
        "Sector",
        sorted(df["sector"].dropna().unique()),
        default=sorted(df["sector"].dropna().unique()),
    )

    roles = sidebar.multiselect(
        "Derived primary role",
        list(ROLE_COLS.keys()),
        default=list(ROLE_COLS.keys()),
    )

    min_revenue = float(df["revenue_aed_bn"].min())
    max_revenue = float(df["revenue_aed_bn"].max())
    revenue_range = sidebar.slider("Revenue range (AED bn)", min_revenue, max_revenue, (min_revenue, max_revenue))

    min_win = sidebar.slider("Minimum win probability", 0.0, 1.0, 0.0, 0.01)

    page = sidebar.radio(
        "Workspace",
        [
            "Portfolio Overview",
            "Opportunity Map",
            "Service Design Studio",
            "Revenue Planner",
            "Data Lab",
        ],
    )

    filtered = df[
        df["sector"].isin(sectors)
        & df["primary_role_derived"].isin(roles)
        & df["revenue_aed_bn"].between(revenue_range[0], revenue_range[1])
        & (df["win_probability"] >= min_win)
    ].copy()

    return filtered, page


def sector_bar(filtered):
    df = filtered.groupby("sector", as_index=False).agg(north_star_value=("north_star_value", "sum")).sort_values("north_star_value", ascending=False)
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("sector:N", sort="-y", title=""),
        y=alt.Y("north_star_value:Q", title="North Star value"),
        color=alt.Color("sector:N", legend=None),
        tooltip=["sector", alt.Tooltip("north_star_value:Q", format=",.0f")],
    ).properties(title="North Star value by sector", height=320)


def role_heatmap(filtered):
    df = filtered.groupby(["sector", "primary_role_derived"], as_index=False).size().rename(columns={"size": "accounts"})
    heat = alt.Chart(df).mark_rect().encode(
        x=alt.X("primary_role_derived:N", title="Primary recommendation"),
        y=alt.Y("sector:N", title="Sector"),
        color=alt.Color("accounts:Q", scale=alt.Scale(scheme="blues"), title="Accounts"),
        tooltip=["sector", "primary_role_derived", "accounts"],
    )
    text = alt.Chart(df).mark_text(fontSize=11).encode(
        x="primary_role_derived:N",
        y="sector:N",
        text="accounts:Q",
        color=alt.condition(alt.datum.accounts >= 2, alt.value("white"), alt.value("#111827")),
    )
    return (heat + text).properties(title="Sector x primary recommendation", height=320)


def archetype_bubble(filtered):
    df = filtered.groupby("need_archetype_derived", as_index=False).agg(
        accounts=("company_name", "count"),
        avg_urgency=("urgency_score", "mean"),
        avg_savings=("estimated_annual_savings_aed", "mean"),
        avg_weighted_acv=("weighted_acv", "mean"),
    )
    return alt.Chart(df).mark_circle(opacity=0.85, stroke="white", strokeWidth=1).encode(
        x=alt.X("avg_urgency:Q", title="Average urgency"),
        y=alt.Y("avg_savings:Q", title="Average savings"),
        size=alt.Size("accounts:Q", scale=alt.Scale(range=[500, 2600]), title="Accounts"),
        color=alt.Color("need_archetype_derived:N", title="Archetype"),
        tooltip=[
            "need_archetype_derived",
            "accounts",
            alt.Tooltip("avg_urgency:Q", format=".1f"),
            alt.Tooltip("avg_savings:Q", format=",.0f"),
            alt.Tooltip("avg_weighted_acv:Q", format=",.0f"),
        ],
    ).properties(title="Archetype opportunity map", height=350)


def priority_table(filtered):
    cols = [
        "company_name", "sector", "primary_role_derived", "secondary_role_derived",
        "priority_band", "priority_index", "weighted_acv", "estimated_annual_savings_aed"
    ]
    out = filtered[cols].sort_values("priority_index", ascending=False).copy()
    out["priority_index"] = out["priority_index"].round(1)
    out["weighted_acv"] = out["weighted_acv"].map(aed)
    out["estimated_annual_savings_aed"] = out["estimated_annual_savings_aed"].map(aed)
    return out


def portfolio_scatter(filtered):
    df = filtered.copy()
    return alt.Chart(df).mark_circle(opacity=0.8, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("urgency_score:Q", title="Urgency score"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV"),
        size=alt.Size("estimated_annual_savings_aed:Q", scale=alt.Scale(range=[80, 1400]), title="Savings"),
        color=alt.Color("primary_role_derived:N", title="Primary role"),
        tooltip=[
            "company_name", "sector", "primary_role_derived", "secondary_role_derived",
            alt.Tooltip("weighted_acv:Q", format=",.0f"),
            alt.Tooltip("estimated_annual_savings_aed:Q", format=",.0f"),
            alt.Tooltip("priority_index:Q", format=".1f"),
        ],
    ).properties(title="Urgency vs weighted ACV", height=380)


def quadrant_chart(filtered):
    med_u = float(filtered["urgency_score"].median())
    med_g = float(filtered["cost_gap_vs_full_time"].median())
    base = alt.Chart(filtered).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.6).encode(
        x=alt.X("urgency_score:Q", title="Urgency score"),
        y=alt.Y("cost_gap_vs_full_time:Q", title="Savings gap vs full-time cost"),
        size=alt.Size("weighted_acv:Q", scale=alt.Scale(range=[70, 1200]), title="Weighted ACV"),
        color=alt.Color("priority_band:N", title="Priority band"),
        tooltip=["company_name", "priority_band", alt.Tooltip("cost_gap_vs_full_time:Q", format=",.0f"), alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    vr = alt.Chart(pd.DataFrame({"x": [med_u]})).mark_rule(strokeDash=[6, 6], color="#9CA3AF").encode(x="x:Q")
    hr = alt.Chart(pd.DataFrame({"y": [med_g]})).mark_rule(strokeDash=[6, 6], color="#9CA3AF").encode(y="y:Q")
    return (vr + hr + base).properties(title="Urgency vs savings gap quadrant", height=360)


def pipeline_month_chart(filtered):
    df = filtered.groupby("close_month_label", as_index=False).agg(weighted_acv=("weighted_acv", "sum"))
    order = pd.DataFrame({"close_month_label": ["M1", "M2", "M3", "M4", "M5", "M6"]})
    df = order.merge(df, on="close_month_label", how="left").fillna(0)
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color="#2563EB").encode(
        x=alt.X("close_month_label:N", title="Expected close month"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV"),
        tooltip=["close_month_label", alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    line = alt.Chart(df).mark_line(point=True, color="#EF4444", strokeWidth=2.5).encode(
        x="close_month_label:N", y="weighted_acv:Q"
    )
    return (bars + line).properties(title="Weighted pipeline by expected close month", height=320)


def close_bucket_chart(filtered):
    df = filtered.groupby("close_bucket", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return alt.Chart(df).mark_arc(innerRadius=60).encode(
        theta=alt.Theta("accounts:Q"),
        color=alt.Color("close_bucket:N", title="Close window"),
        tooltip=["close_bucket", "accounts"],
    ).properties(title="Close-window mix", height=320)


def select_company(filtered):
    companies = sorted(filtered["company_name"].tolist())
    default_company = companies[0] if "selected_company_scratch" not in st.session_state or st.session_state.selected_company_scratch not in companies else st.session_state.selected_company_scratch
    selected = st.sidebar.selectbox("Focus company", companies, index=companies.index(default_company))
    st.session_state.selected_company_scratch = selected
    return filtered.loc[filtered["company_name"] == selected].iloc[0]


def company_role_bars(row):
    df = pd.DataFrame({
        "Role": list(ROLE_COLS.keys()),
        "Need score": [float(safe_value(row, ROLE_COLS[r], 0)) for r in ROLE_COLS],
    }).sort_values("Need score", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X("Need score:Q", title="Need score", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Role:N", sort=None, title=""),
        color=alt.Color("Role:N", legend=None),
        tooltip=["Role", alt.Tooltip("Need score:Q", format=".1f")],
    )
    text = alt.Chart(df).mark_text(dx=8, align="left").encode(
        x="Need score:Q", y=alt.Y("Role:N", sort=None), text=alt.Text("Need score:Q", format=".1f")
    )
    return (bars + text).properties(title="Role-demand profile", height=300)


def company_cost_chart(row):
    df = pd.DataFrame([
        ["Full-time executive stack", float(safe_value(row, "full_time_equivalent_cost_aed", 0)), "Cost"],
        ["Fractional + AI model", float(safe_value(row, "fractional_ai_solution_cost_aed", 0)), "Cost"],
        ["Estimated annual savings", float(safe_value(row, "estimated_annual_savings_aed", 0)), "Value"],
        ["Weighted ACV", float(safe_value(row, "weighted_acv", 0)), "Value"],
    ], columns=["Metric", "Value", "Type"])
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("Metric:N", title=""),
        y=alt.Y("Value:Q", title="AED"),
        color=alt.Color("Type:N", scale=alt.Scale(domain=["Cost", "Value"], range=["#EF4444", "#10B981"])),
        tooltip=["Metric", alt.Tooltip("Value:Q", format=",.0f")],
    ).properties(title="Cost and value benchmark", height=320)


def company_funnel(row):
    touches = max(int(safe_value(row, "sales_touchpoints_90d", 0)), 1)
    responses = max(int(round(touches * float(safe_value(row, "response_probability", 0)) * 0.9)), 1)
    meetings = max(int(safe_value(row, "meetings_booked_90d", 0)), 1 if responses > 1 else 0)
    proposals = max(int(safe_value(row, "proposal_count_90d", 0)), 1 if meetings > 1 else 0)
    closes = max(float(safe_value(row, "win_probability", 0)) * max(1, proposals), 0.5)
    df = pd.DataFrame([
        ["Touches", touches],
        ["Responses", responses],
        ["Meetings", meetings],
        ["Proposals", proposals],
        ["Expected closes", closes],
    ], columns=["Stage", "Value"])
    return alt.Chart(df).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X("Value:Q", title="Volume / expected outcome"),
        y=alt.Y("Stage:N", sort="-x", title=""),
        color=alt.Color("Stage:N", legend=None),
        tooltip=["Stage", alt.Tooltip("Value:Q", format=".1f")],
    ).properties(title="Commercial funnel", height=280)


def company_quarter_chart(row):
    df = pd.DataFrame({
        "Quarter": ["Q1", "Q2", "Q3", "Q4"],
        "Pipeline inquiries": [
            int(safe_value(row, "q1_pipeline_inquiries", 0)),
            int(safe_value(row, "q2_pipeline_inquiries", 0)),
            int(safe_value(row, "q3_pipeline_inquiries", 0)),
            int(safe_value(row, "q4_pipeline_inquiries", 0)),
        ],
        "Revenue growth %": [
            float(safe_value(row, "rev_growth_q1_pct", 0)),
            float(safe_value(row, "rev_growth_q2_pct", 0)),
            float(safe_value(row, "rev_growth_q3_pct", 0)),
            float(safe_value(row, "rev_growth_q4_pct", 0)),
        ],
    })
    bars = alt.Chart(df).mark_bar(color="#2563EB", opacity=0.75).encode(
        x=alt.X("Quarter:N", title=""),
        y=alt.Y("Pipeline inquiries:Q", title="Pipeline inquiries"),
        tooltip=["Quarter", "Pipeline inquiries", alt.Tooltip("Revenue growth %:Q", format=".1f")],
    )
    line = alt.Chart(df).mark_line(color="#F59E0B", point=True, strokeWidth=3).encode(
        x="Quarter:N", y=alt.Y("Revenue growth %:Q", title="Revenue growth %")
    )
    return alt.layer(bars, line).resolve_scale(y="independent").properties(title="Quarterly commercial motion", height=320)


def data_quality_table(df):
    return pd.DataFrame([
        ["Rows", len(df)],
        ["Columns", len(df.columns)],
        ["Missing cells", int(df.isna().sum().sum())],
        ["Duplicate rows", int(df.duplicated().sum())],
        ["Distinct sectors", int(df['sector'].nunique())],
        ["Distinct companies", int(df['company_name'].nunique())],
    ], columns=["Check", "Value"])


def missingness_chart(df):
    miss = (df.isna().mean() * 100).reset_index()
    miss.columns = ["Column", "Missing %"]
    miss = miss.sort_values("Missing %", ascending=False).head(15)
    return alt.Chart(miss).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X("Missing %:Q", title="Missing %"),
        y=alt.Y("Column:N", sort="-x", title=""),
        color=alt.condition(alt.datum['Missing %'] > 0, alt.value('#F59E0B'), alt.value('#10B981')),
        tooltip=["Column", alt.Tooltip("Missing %:Q", format=".2f")],
    ).properties(title="Missingness profile", height=360)


def cleaned_export_table(filtered):
    cols = [
        "company_name", "sector", "revenue_aed_bn", "primary_role_derived", "secondary_role_derived",
        "need_archetype_derived", "priority_band", "priority_index", "weighted_acv", "weighted_ltv",
        "estimated_annual_savings_aed", "cost_gap_vs_full_time", "close_bucket", "delivery_model"
    ]
    out = filtered[cols].sort_values("priority_index", ascending=False).copy()
    out["priority_index"] = out["priority_index"].round(1)
    return out


def big_number_strip(filtered):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Companies", f"{len(filtered)}")
    c2.metric("North Star value", aed(filtered["north_star_value"].sum()))
    c3.metric("Weighted ACV", aed(filtered["weighted_acv"].sum()))
    c4.metric("Savings pool", aed(filtered["estimated_annual_savings_aed"].sum()))
    c5.metric("Avg priority", f"{filtered['priority_index'].mean():.1f}")


def write_header():
    st.title("Dubai CXO Control Tower")
    st.caption(
        "A full scratch rebuild focused on portfolio prioritization, service design, value logic, and light-weight pipeline planning for Dubai corporates."
    )


def company_summary_card(row):
    st.subheader(row["company_name"])
    left, mid, right = st.columns([1.1, 1.1, 1.8])
    with left:
        st.metric("Primary recommendation", row["primary_role_derived"], f"Score {row['primary_role_score']:.1f}")
        st.metric("Secondary recommendation", row["secondary_role_derived"], f"Score {row['secondary_role_score']:.1f}")
    with mid:
        st.metric("Expected ACV", aed(row["expected_annual_contract_value_aed"]), f"Weighted {aed(row['weighted_acv'])}")
        st.metric("Savings", aed(row["estimated_annual_savings_aed"]), f"Gap {aed(row['cost_gap_vs_full_time'])}")
    with right:
        st.markdown("### Recommendation")
        st.write(f"**Archetype:** {row['need_archetype_derived']}")
        st.write(f"**Delivery model:** {row['delivery_model']}")
        st.write(f"**Offer design:** {row['recommendation_logic']}")
        if "recommended_service_package" in row.index:
            st.write(f"**Package:** {row['recommended_service_package']}")
        if "ideal_next_action" in row.index:
            st.write(f"**Next action:** {row['ideal_next_action']}")


def main():
    write_header()
    raw = load_data()
    df = derive_fields(raw)
    filtered, page = filter_data(df)

    if filtered.empty:
        st.warning("No companies match the current filters.")
        return

    focus_row = select_company(filtered)

    if page == "Portfolio Overview":
        big_number_strip(filtered)
        a, b = st.columns([0.56, 0.44], gap="large")
        with a:
            st.altair_chart(sector_bar(filtered), use_container_width=True)
        with b:
            st.altair_chart(archetype_bubble(filtered), use_container_width=True)
        c, d = st.columns([0.52, 0.48], gap="large")
        with c:
            st.altair_chart(role_heatmap(filtered), use_container_width=True)
        with d:
            st.dataframe(priority_table(filtered), use_container_width=True, hide_index=True, height=340)

    elif page == "Opportunity Map":
        st.subheader("Portfolio opportunity mapping")
        st.write("This workspace is about where to focus attention first, using urgency, savings, weighted value, and recommendation logic.")
        a, b = st.columns([0.55, 0.45], gap="large")
        with a:
            st.altair_chart(portfolio_scatter(filtered), use_container_width=True)
        with b:
            st.altair_chart(quadrant_chart(filtered), use_container_width=True)
        st.dataframe(
            filtered[[
                "company_name", "sector", "primary_role_derived", "secondary_role_derived",
                "priority_band", "priority_index", "weighted_acv", "estimated_annual_savings_aed"
            ]].sort_values(["priority_index", "weighted_acv"], ascending=[False, False]),
            use_container_width=True,
            hide_index=True,
        )

    elif page == "Service Design Studio":
        company_summary_card(focus_row)
        a, b = st.columns([0.48, 0.52], gap="large")
        with a:
            st.altair_chart(company_role_bars(focus_row), use_container_width=True)
        with b:
            st.altair_chart(company_cost_chart(focus_row), use_container_width=True)
        exp1, exp2, exp3 = st.columns(3, gap="large")
        with exp1:
            st.info(f"**Primary wedge**\n\nLead with **{focus_row['primary_role_derived']}** because it is the highest-scoring executive need in this account.")
        with exp2:
            st.info(f"**Expansion path**\n\nUse **{focus_row['secondary_role_derived']}** as the second-stage offer once the first workstream proves value.")
        with exp3:
            ai_roles = safe_value(focus_row, 'ai_supported_roles', 'AI-enabled support roles')
            st.info(f"**AI layer**\n\nPosition AI support through **{ai_roles}** to keep the model scalable and lower-cost.")
        st.dataframe(
            pd.DataFrame({
                "Metric": [
                    "Priority index", "Win probability %", "Response probability %", "Expected ROI", "Weighted LTV", "Value at risk"
                ],
                "Value": [
                    round(float(focus_row["priority_index"]), 1),
                    round(float(focus_row["win_pct"]), 1),
                    round(float(focus_row["response_pct"]), 1),
                    round(float(safe_value(focus_row, "expected_roi_multiple", 0)), 2),
                    aed(focus_row["weighted_ltv"]),
                    aed(focus_row["value_at_risk"]),
                ]
            }),
            use_container_width=True,
            hide_index=True,
        )

    elif page == "Revenue Planner":
        company_summary_card(focus_row)
        a, b = st.columns([0.52, 0.48], gap="large")
        with a:
            st.altair_chart(pipeline_month_chart(filtered), use_container_width=True)
        with b:
            st.altair_chart(close_bucket_chart(filtered), use_container_width=True)
        c, d = st.columns([0.48, 0.52], gap="large")
        with c:
            st.altair_chart(company_funnel(focus_row), use_container_width=True)
        with d:
            st.altair_chart(company_quarter_chart(focus_row), use_container_width=True)

    elif page == "Data Lab":
        st.subheader("Synthetic data quality and transformation lab")
        a, b = st.columns([0.34, 0.66], gap="large")
        with a:
            st.dataframe(data_quality_table(filtered), use_container_width=True, hide_index=True)
        with b:
            st.altair_chart(missingness_chart(filtered), use_container_width=True)
        st.markdown("### Derived fields preview")
        st.dataframe(cleaned_export_table(filtered), use_container_width=True, hide_index=True, height=360)
        st.download_button(
            "Download transformed dataset",
            cleaned_export_table(filtered).to_csv(index=False).encode("utf-8"),
            file_name="dubai_cxo_transformed_export.csv",
            mime="text/csv",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
