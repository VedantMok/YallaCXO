import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(page_title="Dubai Fractional CXO Prioritization OS", page_icon="📊", layout="wide")


# -----------------------------
# Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


# -----------------------------
# Theme
# -----------------------------
def get_palette(mode: str):
    if mode == "Light":
        return {
            "bg": "#F5F7FB",
            "bg_grad_1": "rgba(59,130,246,0.08)",
            "bg_grad_2": "rgba(20,184,166,0.08)",
            "panel": "rgba(255,255,255,0.88)",
            "border": "rgba(15,23,42,0.08)",
            "text": "#0F172A",
            "muted": "#5B6B7F",
            "accent": "#2563EB",
            "accent_2": "#14B8A6",
            "accent_3": "#7C3AED",
            "success": "#10B981",
            "danger": "#F97316",
            "warn": "#F59E0B",
            "grid": "rgba(15,23,42,0.08)",
            "pill": "rgba(37,99,235,0.06)",
            "hero_start": "#EAF2FF",
            "hero_mid": "#F8FBFF",
            "hero_end": "#EEFFFB",
            "shadow": "0 16px 42px rgba(15,23,42,0.08)",
            "chip": "rgba(37,99,235,0.08)",
        }
    return {
        "bg": "#0B1220",
        "bg_grad_1": "rgba(37,99,235,0.12)",
        "bg_grad_2": "rgba(20,184,166,0.10)",
        "panel": "rgba(15,23,42,0.74)",
        "border": "rgba(148,163,184,0.14)",
        "text": "#E8EEF8",
        "muted": "#A8B7CA",
        "accent": "#60A5FA",
        "accent_2": "#2DD4BF",
        "accent_3": "#A78BFA",
        "success": "#34D399",
        "danger": "#FB923C",
        "warn": "#FBBF24",
        "grid": "rgba(148,163,184,0.12)",
        "pill": "rgba(96,165,250,0.08)",
        "hero_start": "#0F172A",
        "hero_mid": "#111827",
        "hero_end": "#10243B",
        "shadow": "0 18px 46px rgba(2,6,23,0.34)",
        "chip": "rgba(96,165,250,0.10)",
    }


def enable_altair_theme(p):
    def theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": None},
                "title": {
                    "color": p["text"],
                    "fontSize": 18,
                    "font": "Space Grotesk",
                    "anchor": "start",
                    "fontWeight": 700,
                },
                "axis": {
                    "labelColor": p["muted"],
                    "titleColor": p["text"],
                    "gridColor": p["grid"],
                    "domainColor": p["grid"],
                    "tickColor": p["grid"],
                    "labelFont": "Inter",
                    "titleFont": "Inter",
                },
                "legend": {
                    "labelColor": p["muted"],
                    "titleColor": p["text"],
                    "labelFont": "Inter",
                    "titleFont": "Inter",
                },
                "range": {
                    "category": [
                        p["accent"],
                        p["accent_2"],
                        p["accent_3"],
                        p["success"],
                        p["danger"],
                        p["warn"],
                    ]
                },
            }
        }

    try:
        alt.themes.register("dubai_cxo_scope_theme", theme)
    except Exception:
        pass
    alt.themes.enable("dubai_cxo_scope_theme")


def inject_css(p):
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 8% 14%, {p['bg_grad_1']}, transparent 27%),
                radial-gradient(circle at 92% 8%, {p['bg_grad_2']}, transparent 24%),
                linear-gradient(180deg, {p['bg']} 0%, {p['bg']} 100%);
            color: {p['text']};
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 2.2rem;
            max-width: 1500px;
        }}

        section[data-testid="stSidebar"] {{
            display: none;
        }}

        .hero {{
            background: linear-gradient(135deg, {p['hero_start']} 0%, {p['hero_mid']} 55%, {p['hero_end']} 100%);
            border: 1px solid {p['border']};
            border-radius: 30px;
            padding: 1.55rem 1.75rem;
            box-shadow: {p['shadow']};
            margin-bottom: 1rem;
        }}

        .hero-wrap {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }}

        .hero h1 {{
            font-family: 'Space Grotesk', sans-serif;
            margin: 0;
            color: {p['text']};
            font-size: 2.30rem;
        }}

        .hero p {{
            margin: .45rem 0 0 0;
            color: {p['muted']};
            line-height: 1.62;
            max-width: 1000px;
        }}

        .chip {{
            display: inline-flex;
            align-items: center;
            padding: .48rem .76rem;
            border-radius: 999px;
            background: {p['chip']};
            border: 1px solid {p['border']};
            color: {p['text']};
            font-size: .82rem;
        }}

        .banner {{
            background: linear-gradient(135deg, rgba(37,99,235,0.11), rgba(20,184,166,0.10));
            border: 1px solid {p['border']};
            border-radius: 24px;
            padding: 1.2rem 1.25rem;
            box-shadow: {p['shadow']};
            margin-bottom: 1rem;
        }}

        .banner h2 {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.62rem;
            margin: 0;
            color: {p['text']};
        }}

        .banner p {{
            margin: .25rem 0 0 0;
            color: {p['muted']};
            line-height: 1.58;
            max-width: 980px;
        }}

        .pill-row {{
            display: flex;
            gap: .55rem;
            flex-wrap: wrap;
            margin-top: .86rem;
        }}

        .pill {{
            display: inline-flex;
            padding: .48rem .78rem;
            border-radius: 999px;
            background: {p['pill']};
            border: 1px solid {p['border']};
            color: {p['text']};
            font-size: .82rem;
        }}

        .metric {{
            background: {p['panel']};
            border: 1px solid {p['border']};
            border-radius: 22px;
            padding: 1rem .96rem;
            min-height: 128px;
            box-shadow: {p['shadow']};
        }}

        .metric .label {{
            font-size: .74rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            color: {p['muted']};
            margin-bottom: .32rem;
        }}

        .metric .value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.48rem;
            font-weight: 700;
            color: {p['text']};
            line-height: 1.1;
            margin-bottom: .25rem;
        }}

        .metric .sub {{
            font-size: .84rem;
            color: {p['muted']};
            line-height: 1.45;
        }}

        .section-kicker {{
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            color: {p['accent_2']};
            margin-bottom: .26rem;
        }}

        .section-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.36rem;
            color: {p['text']};
            margin: .06rem 0 .18rem 0;
        }}

        .section-copy {{
            color: {p['muted']};
            line-height: 1.58;
            margin-bottom: .95rem;
            max-width: 1040px;
        }}

        .insight {{
            background: {p['panel']};
            border: 1px solid {p['border']};
            border-left: 4px solid {p['accent']};
            border-radius: 18px;
            padding: 1rem 1.02rem;
            box-shadow: {p['shadow']};
            height: 100%;
        }}

        .insight h4 {{
            margin: 0 0 .42rem 0;
            color: {p['text']};
            font-size: 1rem;
        }}

        .insight p {{
            margin: 0;
            color: {p['muted']};
            line-height: 1.56;
        }}

        .callout {{
            background: linear-gradient(135deg, rgba(37,99,235,0.10), rgba(20,184,166,0.10));
            border: 1px solid {p['border']};
            border-left: 4px solid {p['accent']};
            border-radius: 22px;
            padding: 1rem 1.1rem;
            margin: .85rem 0 1rem 0;
            box-shadow: {p['shadow']};
            color: {p['text']};
            line-height: 1.6;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: .4rem;
            margin-bottom: .50rem;
            flex-wrap: wrap;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: {p['panel']};
            border: 1px solid {p['border']};
            border-radius: 14px;
            color: {p['muted']};
            padding: .58rem .92rem;
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(180deg, rgba(37,99,235,0.12), rgba(20,184,166,0.12));
            color: {p['text']};
            border-color: {p['accent']};
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            background: {p['panel']};
            border-color: {p['border']};
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {p['border']};
            border-radius: 18px;
            overflow: hidden;
        }}

        details {{
            background: {p['panel']};
            border: 1px solid {p['border']};
            border-radius: 22px;
            box-shadow: {p['shadow']};
        }}

        details summary {{
            padding: .95rem 1rem;
        }}

        @media (max-width: 920px) {{
            .hero-wrap {{
                flex-direction: column;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Helpers
# -----------------------------
def fmt_aed(x):
    x = float(x)
    if abs(x) >= 1_000_000_000:
        return f"AED {x/1_000_000_000:.2f}B"
    if abs(x) >= 1_000_000:
        return f"AED {x/1_000_000:.2f}M"
    if abs(x) >= 1_000:
        return f"AED {x/1_000:.1f}K"
    return f"AED {x:,.0f}"


def metric_card(label, value, sub):
    st.markdown(
        f"<div class='metric'><div class='label'>{label}</div><div class='value'>{value}</div><div class='sub'>{sub}</div></div>",
        unsafe_allow_html=True,
    )


def insight_card(title, text):
    st.markdown(
        f"<div class='insight'><h4>{title}</h4><p>{text}</p></div>",
        unsafe_allow_html=True,
    )


def section_header(kicker, title, copy):
    st.markdown(
        f"<div class='section-kicker'>{kicker}</div><div class='section-title'>{title}</div><div class='section-copy'>{copy}</div>",
        unsafe_allow_html=True,
    )


def band_from_pct(s, labels):
    return pd.cut(
        s.rank(pct=True),
        bins=[0.0, 0.25, 0.50, 0.75, 1.0],
        labels=labels,
        include_lowest=True,
    )


# -----------------------------
# State and filters
# -----------------------------
def init_state(df):
    if "appearance_mode" not in st.session_state:
        st.session_state.appearance_mode = "Dark"
    if "selected_company" not in st.session_state:
        st.session_state.selected_company = sorted(df["company_name"].tolist())[0]

    defaults = {
        "flt_sector": sorted(df["sector"].dropna().unique()),
        "flt_role": sorted(df["primary_fractional_cxo"].dropna().unique()),
        "flt_urgency": sorted(df["urgency_tier"].dropna().unique()),
        "flt_tier": sorted(df["account_tier"].dropna().unique()),
        "flt_revenue": (
            float(df["revenue_aed_bn"].min()),
            float(df["revenue_aed_bn"].max()),
        ),
        "flt_min_win": 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_filters(df):
    st.session_state.flt_sector = sorted(df["sector"].dropna().unique())
    st.session_state.flt_role = sorted(df["primary_fractional_cxo"].dropna().unique())
    st.session_state.flt_urgency = sorted(df["urgency_tier"].dropna().unique())
    st.session_state.flt_tier = sorted(df["account_tier"].dropna().unique())
    st.session_state.flt_revenue = (
        float(df["revenue_aed_bn"].min()),
        float(df["revenue_aed_bn"].max()),
    )
    st.session_state.flt_min_win = 0.0


def filtered_df(df):
    return df[
        df["sector"].isin(st.session_state.flt_sector)
        & df["primary_fractional_cxo"].isin(st.session_state.flt_role)
        & df["urgency_tier"].isin(st.session_state.flt_urgency)
        & df["account_tier"].isin(st.session_state.flt_tier)
        & df["revenue_aed_bn"].between(
            st.session_state.flt_revenue[0], st.session_state.flt_revenue[1]
        )
        & (df["win_probability"] >= st.session_state.flt_min_win)
    ].copy()


# -----------------------------
# Engineering
# -----------------------------
ROLE_MAP = {
    "cfo_need_score": "CFO",
    "cto_need_score": "CTO",
    "chro_need_score": "CHRO",
    "cmo_need_score": "CMO",
    "coo_need_score": "COO",
}


ARCHETYPE_MAP = {
    "CFO": "Finance-stressed firms",
    "CTO": "Tech-transformation firms",
    "CHRO": "People-scaling firms",
    "CMO": "Marketing-efficiency firms",
    "COO": "Operational-efficiency firms",
}


def derive_primary_secondary(row):
    scores = {role: float(row[col]) for col, role in ROLE_MAP.items()}
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ordered[0][0], ordered[1][0], ordered[0][1], ordered[1][1]


def add_engineered_fields(df):
    out = df.copy()

    primary_scores = []
    secondary_scores = []
    recomputed_primary = []
    recomputed_secondary = []

    for _, row in out.iterrows():
        p_role, s_role, p_score, s_score = derive_primary_secondary(row)
        recomputed_primary.append(p_role)
        recomputed_secondary.append(s_role)
        primary_scores.append(p_score)
        secondary_scores.append(s_score)

    out["derived_primary_cxo"] = recomputed_primary
    out["derived_secondary_cxo"] = recomputed_secondary
    out["derived_primary_score"] = primary_scores
    out["derived_secondary_score"] = secondary_scores
    out["need_archetype"] = out["derived_primary_cxo"].map(ARCHETYPE_MAP)

    out["weighted_acv"] = out["expected_annual_contract_value_aed"] * out["win_probability"]
    out["weighted_ltv"] = out["expected_account_ltv_aed"] * out["win_probability"]
    out["solution_roi_proxy"] = out["estimated_annual_savings_aed"] / out["fractional_ai_solution_cost_aed"].replace(0, np.nan)
    out["solution_roi_proxy"] = out["solution_roi_proxy"].replace([np.inf, -np.inf], np.nan).fillna(0)
    out["savings_vs_ft_gap"] = out["full_time_equivalent_cost_aed"] - out["fractional_ai_solution_cost_aed"]
    out["value_at_risk"] = out["expected_account_ltv_aed"] * out["client_churn_risk_score"] / 100.0
    out["response_pct"] = out["response_probability"] * 100
    out["win_pct"] = out["win_probability"] * 100
    out["priority_index"] = (
        0.30 * out["derived_primary_score"]
        + 0.20 * out["urgency_score"]
        + 0.20 * out["win_pct"]
        + 0.15 * out["response_pct"]
        + 0.15 * out["account_health_score"]
    )
    out["priority_band"] = band_from_pct(out["priority_index"], ["Watch", "Build", "Prioritize", "Act now"])
    out["ltv_band"] = band_from_pct(out["expected_account_ltv_aed"], ["Low", "Mid", "High", "Elite"])
    out["close_horizon"] = pd.cut(
        out["expected_close_days"],
        bins=[-1, 30, 60, 90, 9999],
        labels=["0-30d", "31-60d", "61-90d", "90d+"],
    )
    out["service_mix_gap"] = out["derived_primary_score"] - out["derived_secondary_score"]
    out["monthly_expected_close"] = np.clip(np.ceil(out["expected_close_days"] / 30), 1, 6).astype(int)
    return out


# -----------------------------
# Narrative
# -----------------------------
def narrative(row):
    return (
        f"{row['company_name']} is positioned as a lead-prioritization and service-design case. "
        f"The strongest need is {row['derived_primary_cxo']} ({row['derived_primary_score']:.1f}), "
        f"the secondary opportunity is {row['derived_secondary_cxo']} ({row['derived_secondary_score']:.1f}), "
        f"and the account sits inside the {row['need_archetype'].lower()} group."
    )


def executive_hook(row):
    return (
        f"Expected ACV is {fmt_aed(row['expected_annual_contract_value_aed'])}, weighted ACV is {fmt_aed(row['weighted_acv'])}, "
        f"estimated annual savings are {fmt_aed(row['estimated_annual_savings_aed'])}, "
        f"and the solution is benchmarked against {fmt_aed(row['full_time_equivalent_cost_aed'])} in full-time CXO cost."
    )


# -----------------------------
# Charts
# -----------------------------
def portfolio_leaderboard(filtered, row, p):
    top = (
        filtered[["company_name", "priority_index", "weighted_acv"]]
        .sort_values("priority_index", ascending=False)
        .head(15)
        .copy()
    )
    top["selected"] = np.where(top["company_name"] == row["company_name"], "Selected", "Peer")
    bars = alt.Chart(top).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("priority_index:Q", title="Priority index"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color(
            "selected:N",
            scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent"], p["danger"]]),
            legend=None,
        ),
        tooltip=["company_name", alt.Tooltip("priority_index:Q", format=".1f"), alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    return bars.properties(title="Top accounts by priority index", height=360)


def urgency_value_scatter(filtered, row, p):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    base = alt.Chart(df).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("urgency_score:Q", title="Urgency score"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV (AED)"),
        size=alt.Size("estimated_annual_savings_aed:Q", scale=alt.Scale(range=[80, 1300]), title="Savings"),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("derived_primary_cxo:N", title="Primary CXO")),
        tooltip=["company_name", "derived_primary_cxo", "need_archetype", alt.Tooltip("weighted_acv:Q", format=",.0f"), alt.Tooltip("estimated_annual_savings_aed:Q", format=",.0f")],
    )
    label = alt.Chart(df[df["selected"]]).mark_text(dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]).encode(
        x="urgency_score:Q", y="weighted_acv:Q", text="company_name:N"
    )
    return (base + label).properties(title="Urgency versus weighted ACV", height=360)


def sector_role_heatmap(filtered):
    df = filtered.groupby(["sector", "derived_primary_cxo"], as_index=False).size().rename(columns={"size": "accounts"})
    heat = alt.Chart(df).mark_rect(cornerRadius=6).encode(
        x=alt.X("derived_primary_cxo:N", title="Primary CXO"),
        y=alt.Y("sector:N", title="Sector", sort="-x"),
        color=alt.Color("accounts:Q", scale=alt.Scale(scheme="tealblues"), title="Accounts"),
        tooltip=["sector", "derived_primary_cxo", "accounts"],
    )
    text = alt.Chart(df).mark_text(fontSize=11).encode(
        x="derived_primary_cxo:N",
        y="sector:N",
        text="accounts:Q",
        color=alt.condition(alt.datum.accounts > 2, alt.value("white"), alt.value("#0F172A")),
    )
    return (heat + text).properties(title="Sector by primary-CXO demand", height=360)


def north_star_bar(filtered, p):
    df = (
        filtered.groupby("sector", as_index=False)
        .agg(
            weighted_acv=("weighted_acv", "sum"),
            savings=("estimated_annual_savings_aed", "sum"),
        )
        .sort_values("weighted_acv", ascending=False)
        .head(10)
    )
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=36).encode(
        x=alt.X("sector:N", title=""),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV (AED)"),
        color=alt.Color("sector:N", title=""),
        tooltip=["sector", alt.Tooltip("weighted_acv:Q", format=",.0f"), alt.Tooltip("savings:Q", format=",.0f")],
    )
    return bars.properties(title="North Star by sector: weighted ACV", height=320)


def savings_histogram(filtered, p):
    return alt.Chart(filtered).mark_bar(opacity=0.85, color=p["accent"]).encode(
        x=alt.X("estimated_annual_savings_aed:Q", bin=alt.Bin(maxbins=20), title="Estimated annual savings (AED)"),
        y=alt.Y("count():Q", title="Accounts"),
        tooltip=[alt.Tooltip("count():Q", title="Accounts")],
    ).properties(title="Savings distribution", height=300)


def acv_boxplot(filtered):
    return alt.Chart(filtered).mark_boxplot(extent="min-max").encode(
        x=alt.X("derived_primary_cxo:N", title="Primary CXO"),
        y=alt.Y("expected_annual_contract_value_aed:Q", title="Expected ACV (AED)"),
        color=alt.Color("derived_primary_cxo:N", title=""),
        tooltip=["derived_primary_cxo", alt.Tooltip("expected_annual_contract_value_aed:Q", format=",.0f")],
    ).properties(title="ACV spread by primary CXO", height=300)


def quarterly_motion_chart(row, p):
    df = pd.DataFrame(
        {
            "Quarter": ["Q1", "Q2", "Q3", "Q4"],
            "Pipeline inquiries": [
                int(row["q1_pipeline_inquiries"]),
                int(row["q2_pipeline_inquiries"]),
                int(row["q3_pipeline_inquiries"]),
                int(row["q4_pipeline_inquiries"]),
            ],
            "Revenue growth %": [
                float(row["rev_growth_q1_pct"]),
                float(row["rev_growth_q2_pct"]),
                float(row["rev_growth_q3_pct"]),
                float(row["rev_growth_q4_pct"]),
            ],
        }
    )
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=42, opacity=0.78, color=p["accent"]).encode(
        x=alt.X("Quarter:N", title=""),
        y=alt.Y("Pipeline inquiries:Q", title="Pipeline inquiries"),
        tooltip=["Quarter", "Pipeline inquiries", alt.Tooltip("Revenue growth %:Q", format=".1f")],
    )
    line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color=p["success"]).encode(
        x="Quarter:N",
        y=alt.Y("Revenue growth %:Q", title="Revenue growth %"),
    )
    return alt.layer(bars, line).resolve_scale(y="independent").properties(title="Quarterly commercial motion", height=300)


def driver_donut_selected(row):
    df = pd.DataFrame(
        {
            "Driver": ["Savings", "Weighted ACV", "Weighted LTV", "Value at risk"],
            "Value": [
                float(row["estimated_annual_savings_aed"]),
                float(row["weighted_acv"]),
                float(row["weighted_ltv"]),
                float(row["value_at_risk"]),
            ],
        }
    )
    return alt.Chart(df).mark_arc(innerRadius=68).encode(
        theta=alt.Theta("Value:Q"),
        color=alt.Color("Driver:N", title=""),
        tooltip=["Driver", alt.Tooltip("Value:Q", format=",.0f")],
    ).properties(title="Selected-company value mix", height=300)


def segment_bubble(filtered):
    df = (
        filtered.groupby("need_archetype", as_index=False)
        .agg(
            accounts=("company_name", "count"),
            avg_urgency=("urgency_score", "mean"),
            avg_savings=("estimated_annual_savings_aed", "mean"),
            avg_acv=("expected_annual_contract_value_aed", "mean"),
        )
    )
    return alt.Chart(df).mark_circle(opacity=0.84, stroke="white", strokeWidth=1).encode(
        x=alt.X("avg_urgency:Q", title="Average urgency"),
        y=alt.Y("avg_savings:Q", title="Average savings (AED)"),
        size=alt.Size("accounts:Q", scale=alt.Scale(range=[400, 2600]), title="Accounts"),
        color=alt.Color("need_archetype:N", title="Archetype"),
        tooltip=["need_archetype", "accounts", alt.Tooltip("avg_urgency:Q", format=".1f"), alt.Tooltip("avg_savings:Q", format=",.0f"), alt.Tooltip("avg_acv:Q", format=",.0f")],
    ).properties(title="Archetype opportunity map", height=340)


def segment_stack(filtered):
    df = filtered.groupby(["sector", "need_archetype"], as_index=False).size().rename(columns={"size": "accounts"})
    return alt.Chart(df).mark_bar().encode(
        x=alt.X("sector:N", title=""),
        y=alt.Y("accounts:Q", title="Accounts"),
        color=alt.Color("need_archetype:N", title="Archetype"),
        tooltip=["sector", "need_archetype", "accounts"],
    ).properties(title="Sector composition by archetype", height=320)


def archetype_priority_dot(filtered, p):
    df = (
        filtered.groupby("need_archetype", as_index=False)
        .agg(
            priority=("priority_index", "mean"),
            weighted_acv=("weighted_acv", "mean"),
        )
        .sort_values("priority", ascending=True)
    )
    dots = alt.Chart(df).mark_circle(size=220, color=p["accent"]).encode(
        x=alt.X("priority:Q", title="Average priority index"),
        y=alt.Y("need_archetype:N", sort=None, title=""),
        tooltip=["need_archetype", alt.Tooltip("priority:Q", format=".1f"), alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dx=10, align="left", color=p["text"], fontSize=11).encode(
        x="priority:Q",
        y=alt.Y("need_archetype:N", sort=None),
        text=alt.Text("weighted_acv:Q", format=",.0f"),
    )
    return (dots + text).properties(title="Average priority by archetype", height=300)


def role_profile_chart(row, p):
    df = pd.DataFrame(
        {
            "Role": ["CFO", "CTO", "CHRO", "CMO", "COO"],
            "Need": [
                float(row["cfo_need_score"]),
                float(row["cto_need_score"]),
                float(row["chro_need_score"]),
                float(row["cmo_need_score"]),
                float(row["coo_need_score"]),
            ],
        }
    ).sort_values("Need", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X("Need:Q", title="Need score", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Role:N", sort=None, title=""),
        color=alt.Color("Role:N", title=""),
        tooltip=["Role", alt.Tooltip("Need:Q", format=".1f")],
    )
    text = alt.Chart(df).mark_text(dx=8, align="left", fontSize=11, color=p["text"]).encode(
        x="Need:Q", y=alt.Y("Role:N", sort=None), text=alt.Text("Need:Q", format=".1f")
    )
    return (bars + text).properties(title="Selected-company role profile", height=300)


def role_priority_matrix(row, p):
    df = pd.DataFrame(
        [
            {"Role": "CFO", "Need": float(row["cfo_need_score"]), "Enablement": (float(row["data_maturity_score"]) + float(row["cash_flow_volatility_score"])) / 2},
            {"Role": "CTO", "Need": float(row["cto_need_score"]), "Enablement": (float(row["digital_maturity_score"]) + float(row["cyber_risk_score"])) / 2},
            {"Role": "CHRO", "Need": float(row["chro_need_score"]), "Enablement": (100 - float(row["attrition_rate_pct"]) * 2 + float(row["hiring_velocity_score"])) / 2},
            {"Role": "CMO", "Need": float(row["cmo_need_score"]), "Enablement": min(100, float(row["campaign_roi_x"]) * 22 + float(row["lead_conversion_pct"]) * 4)},
            {"Role": "COO", "Need": float(row["coo_need_score"]), "Enablement": (float(row["process_efficiency_score"]) + float(row["project_backlog_score"])) / 2},
        ]
    )
    df["Priority"] = df["Need"] * 0.7 + df["Enablement"] * 0.3
    scatter = alt.Chart(df).mark_circle(opacity=0.88, stroke="white", strokeWidth=1).encode(
        x=alt.X("Enablement:Q", title="Enablement", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Need:Q", title="Need", scale=alt.Scale(domain=[0, 100])),
        size=alt.Size("Priority:Q", scale=alt.Scale(range=[220, 1500]), title="Priority"),
        color=alt.Color("Role:N", title=""),
        tooltip=["Role", alt.Tooltip("Need:Q", format=".1f"), alt.Tooltip("Enablement:Q", format=".1f"), alt.Tooltip("Priority:Q", format=".1f")],
    )
    label = alt.Chart(df).mark_text(dy=-16, fontSize=11, color=p["text"]).encode(
        x="Enablement:Q", y="Need:Q", text="Role:N"
    )
    return (scatter + label).properties(title="Role priority matrix", height=320)


def service_package_chart(filtered):
    df = filtered.groupby("recommended_service_package", as_index=False).size().rename(columns={"size": "accounts"}).sort_values("accounts", ascending=False)
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=46).encode(
        x=alt.X("recommended_service_package:N", sort="-y", title=""),
        y=alt.Y("accounts:Q", title="Accounts"),
        color=alt.Color("recommended_service_package:N", title=""),
        tooltip=["recommended_service_package", "accounts"],
    ).properties(title="Recommended service packages", height=320)


def cost_savings_chart(row, p):
    df = pd.DataFrame(
        [
            {"Metric": "Full-time CXO cost", "Value": float(row["full_time_equivalent_cost_aed"]), "Type": "Cost"},
            {"Metric": "Fractional + AI cost", "Value": float(row["fractional_ai_solution_cost_aed"]), "Type": "Cost"},
            {"Metric": "Estimated annual savings", "Value": float(row["estimated_annual_savings_aed"]), "Type": "Value"},
        ]
    )
    df["Color"] = df["Type"].map({"Cost": p["danger"], "Value": p["success"]})
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=62).encode(
        x=alt.X("Metric:N", title=""),
        y=alt.Y("Value:Q", title="AED"),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Metric", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-10, color=p["text"], fontSize=11).encode(
        x="Metric:N", y="Value:Q", text=alt.Text("Value:
