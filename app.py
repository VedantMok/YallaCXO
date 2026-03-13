import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import pydeck as pdk

st.set_page_config(page_title="Yalla CXO Impact OS", page_icon="🚀", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def get_palette(mode: str):
    if mode == "Light":
        return {
            "bg": "#F5F7FB",
            "bg_grad_1": "rgba(59,130,246,0.08)",
            "bg_grad_2": "rgba(20,184,166,0.08)",
            "panel": "rgba(255,255,255,0.88)",
            "panel_solid": "#FFFFFF",
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
        "panel_solid": "#111827",
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
        alt.themes.register("yalla_impact_os_tabs", theme)
    except Exception:
        pass
    alt.themes.enable("yalla_impact_os_tabs")


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
            max-width: 1520px;
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
            font-size: 2.35rem;
        }}

        .hero p {{
            margin: .45rem 0 0 0;
            color: {p['muted']};
            line-height: 1.62;
            max-width: 980px;
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
            font-size: 1.52rem;
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
            margin-bottom: .55rem;
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


def z_score_pct(series, value):
    s = pd.Series(series).astype(float)
    std = float(s.std())
    if std == 0 or np.isnan(std):
        return 50.0
    z = (float(value) - float(s.mean())) / std
    return float(max(0, min(100, 50 + 18 * z)))


def role_score(row, role_name):
    mapping = {
        "CFO": float(row["cfo_need_score"]),
        "CTO": float(row["cto_need_score"]),
        "CHRO": float(row["chro_need_score"]),
        "CMO": float(row["cmo_need_score"]),
        "COO": float(row["coo_need_score"]),
    }
    return float(mapping.get(role_name, 0))


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


def build_model(row, filtered):
    savings = float(row["estimated_annual_savings_aed"])
    ai_attach = float(row["ai_attach_value_aed"])
    conv_uplift = (
        float(row["recommended_acv_aed"])
        * float(row["baseline_conversion_probability"])
        * (float(row["incremental_uplift_pct"]) / 100.0)
    )
    speed_capture = float(row["forecast_2q_revenue_aed"]) * min(
        0.34, float(row["win_probability"]) * 0.55
    )
    process_uplift = savings * (float(row["automation_potential_score"]) / 100.0) * 0.18
    people_risk = (
        float(row["expected_account_ltv_aed"])
        * (float(row["client_churn_risk_score"]) / 100.0)
        * 0.08
    )
    total = savings + ai_attach + conv_uplift + speed_capture + process_uplift + people_risk

    proof = (
        0.34
        * z_score_pct(filtered["estimated_annual_savings_aed"], row["estimated_annual_savings_aed"])
        + 0.33 * z_score_pct(filtered["expected_roi_multiple"], row["expected_roi_multiple"])
        + 0.33 * z_score_pct(filtered["win_probability"], row["win_probability"])
    )
    urgency = (
        0.35 * float(row["urgency_score"])
        + 0.20 * float(row["cash_flow_volatility_score"])
        + 0.15 * float(row["compliance_risk_score"])
        + 0.15 * float(row["project_backlog_score"])
        + 0.15 * max(0, 100 - float(row["on_time_delivery_pct"]))
    )
    readiness = (
        0.28 * float(row["digital_maturity_score"])
        + 0.22 * float(row["data_maturity_score"])
        + 0.20 * float(row["account_health_score"])
        + 0.15 * float(row["cross_sell_readiness_score"])
        + 0.15 * float(row["response_probability"]) * 100
    )
    feasibility = (
        0.34 * (100 - float(row["expansion_complexity_score"]))
        + 0.22 * float(row["data_maturity_score"])
        + 0.22 * float(row["account_health_score"])
        + 0.22 * float(row["response_probability"]) * 100
    )
    conviction = 0.34 * proof + 0.33 * urgency + 0.33 * readiness

    conservative = total * 0.78
    base = total
    aggressive = total * 1.24
    payback = total / max(1.0, float(row["fractional_ai_solution_cost_aed"]))

    return {
        "savings": savings,
        "ai_attach": ai_attach,
        "conv_uplift": conv_uplift,
        "speed_capture": speed_capture,
        "process_uplift": process_uplift,
        "people_risk": people_risk,
        "total": total,
        "proof": float(max(0, min(100, proof))),
        "urgency": float(max(0, min(100, urgency))),
        "readiness": float(max(0, min(100, readiness))),
        "feasibility": float(max(0, min(100, feasibility))),
        "conviction": float(max(0, min(100, conviction))),
        "conservative": conservative,
        "base": base,
        "aggressive": aggressive,
        "payback": payback,
    }


def narrative(row, model):
    return (
        f"{row['company_name']} should be presented as an impact case, not a staffing case. "
        f"The data suggests a {row['primary_fractional_cxo']}-led intervention addresses "
        f"{str(row['pain_archetype']).lower()}, with {fmt_aed(model['total'])} in modeled value at stake "
        f"across savings, AI monetization, revenue acceleration, and operational improvement."
    )


def recommendations(row, model):
    return {
        "hook": f"This account has {fmt_aed(model['total'])} in modeled value at stake and a conviction score of {model['conviction']:.0f}/100.",
        "why_now": f"Urgency is {row['urgency_score']:.1f}, win probability is {row['win_probability']*100:.1f}%, and the expected close horizon is {int(row['expected_close_days'])} days.",
        "why_solution": f"The strongest need score is {row['primary_need_score']:.1f} for {row['primary_fractional_cxo']}, with AI-supported expansion through {row.get('ai_supported_roles', 'AI-enabled roles')} and {row['secondary_fractional_cxo']} after proof.",
        "proof": f"This case combines {fmt_aed(row['estimated_annual_savings_aed'])} in annual savings, {row['expected_roi_multiple']:.2f}x expected ROI, and {fmt_aed(row['expected_account_ltv_aed'])} expected LTV.",
    }


def add_engineered_fields(df):
    out = df.copy()

    models = []
    for _, r in out.iterrows():
        m = build_model(r, out)
        models.append(
            {
                "impact_total": m["total"],
                "impact_conservative": m["conservative"],
                "impact_base": m["base"],
                "impact_aggressive": m["aggressive"],
                "proof_score": m["proof"],
                "urgency_model_score": m["urgency"],
                "readiness_score": m["readiness"],
                "feasibility_score": m["feasibility"],
                "conviction_score": m["conviction"],
                "impact_payback": m["payback"],
            }
        )
    out = pd.concat([out, pd.DataFrame(models, index=out.index)], axis=1)

    priority = (
        out["impact_total"].rank(pct=True) * 0.33
        + out["expected_account_ltv_aed"].rank(pct=True) * 0.22
        + out["response_probability"].rank(pct=True) * 0.15
        + out["urgency_score"].rank(pct=True) * 0.15
        + out["client_churn_risk_score"].rank(pct=True) * 0.15
    )

    out["segment_name"] = pd.qcut(
        priority.rank(method="first"),
        4,
        labels=["Nurture", "Monitor", "Accelerate", "Scale"],
    )

    out["ltv_band"] = pd.qcut(
        out["expected_account_ltv_aed"].rank(method="first"),
        4,
        labels=["Low", "Mid", "High", "Elite"],
    )

    out["close_horizon"] = pd.cut(
        out["expected_close_days"],
        bins=[-1, 30, 60, 90, 9999],
        labels=["0-30d", "31-60d", "61-90d", "90d+"],
    )

    out["expansion_horizon"] = pd.cut(
        out["next_service_expansion_days"],
        bins=[-1, 30, 60, 120, 9999],
        labels=["0-30d", "31-60d", "61-120d", "120d+"],
    )

    out["risk_band"] = pd.cut(
        out["client_churn_risk_score"],
        bins=[-1, 35, 65, 100],
        labels=["Low risk", "Watch", "High risk"],
    )

    out["response_pct"] = out["response_probability"] * 100
    out["win_pct"] = out["win_probability"] * 100
    out["uplift_value_proxy"] = (
        out["recommended_acv_aed"]
        * out["baseline_conversion_probability"]
        * out["incremental_uplift_pct"]
        / 100.0
    )
    out["impact_proxy"] = (
        out["estimated_annual_savings_aed"]
        + out["ai_attach_value_aed"]
        + out["uplift_value_proxy"]
    )
    out["value_at_risk"] = out["expected_account_ltv_aed"] * out["client_churn_risk_score"] / 100.0
    return out


def comparable_accounts(filtered, row):
    subset = filtered.copy()
    subset["distance"] = (
        (subset["revenue_aed_bn"] - row["revenue_aed_bn"]).abs() * 2
        + (subset["urgency_score"] - row["urgency_score"]).abs() * 0.45
        + (
            subset["expected_annual_contract_value_aed"]
            - row["expected_annual_contract_value_aed"]
        ).abs()
        / 500000
    )
    subset = subset[subset["company_name"] != row["company_name"]].sort_values("distance").head(8)
    out = subset[
        [
            "company_name",
            "sector",
            "segment_name",
            "primary_fractional_cxo",
            "expected_account_ltv_aed",
            "client_churn_risk_score",
            "win_probability",
        ]
    ].copy()
    out["expected_account_ltv_aed"] = out["expected_account_ltv_aed"].map(fmt_aed)
    out["client_churn_risk_score"] = out["client_churn_risk_score"].round(1)
    out["win_probability"] = (out["win_probability"] * 100).round(1).astype(str) + "%"
    return out.rename(
        columns={
            "company_name": "Comparable company",
            "primary_fractional_cxo": "Primary CXO",
            "segment_name": "Segment",
            "expected_account_ltv_aed": "Predicted LTV",
            "client_churn_risk_score": "Churn risk",
            "win_probability": "Win probability",
        }
    )


def donut_chart(df, category, value, title):
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=68)
        .encode(
            theta=alt.Theta(f"{value}:Q"),
            color=alt.Color(f"{category}:N", title=""),
            tooltip=[category, alt.Tooltip(f"{value}:Q", format=",.0f")],
        )
        .properties(title=title, height=300)
    )


def portfolio_rank_chart(filtered, row, p):
    top = (
        filtered[["company_name", "impact_total", "segment_name"]]
        .sort_values("impact_total", ascending=False)
        .head(12)
        .copy()
    )
    top["selected"] = np.where(top["company_name"] == row["company_name"], "Selected", "Peer")
    bars = (
        alt.Chart(top)
        .mark_bar(cornerRadiusEnd=10, height=24)
        .encode(
            x=alt.X("impact_total:Q", title="Modeled impact (AED)"),
            y=alt.Y("company_name:N", sort="-x", title=""),
            color=alt.Color(
                "selected:N",
                scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent"], p["danger"]]),
                legend=None,
            ),
            tooltip=["company_name", "segment_name", alt.Tooltip("impact_total:Q", format=",.0f")],
        )
    )
    text = (
        alt.Chart(top)
        .mark_text(dx=8, align="left", font="Inter", fontSize=11, color=p["text"])
        .encode(
            x="impact_total:Q",
            y=alt.Y("company_name:N", sort="-x"),
            text=alt.Text("impact_total:Q", format=",.0f"),
        )
    )
    return (bars + text).properties(title="Top accounts by modeled impact", height=340)


def impact_stack_chart(model, p):
    df = pd.DataFrame(
        [
            {"Driver": "Executive cost avoided", "Value": model["savings"], "Color": p["success"]},
            {"Driver": "AI attach monetization", "Value": model["ai_attach"], "Color": p["accent_2"]},
            {"Driver": "Incremental conversion value", "Value": model["conv_uplift"], "Color": p["accent"]},
            {"Driver": "Faster revenue capture", "Value": model["speed_capture"], "Color": p["accent_3"]},
            {"Driver": "Process improvement upside", "Value": model["process_uplift"], "Color": p["warn"]},
            {"Driver": "Risk avoided / retention value", "Value": model["people_risk"], "Color": p["danger"]},
        ]
    ).sort_values("Value", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X("Value:Q", title="Modeled annual impact (AED)"),
        y=alt.Y("Driver:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Driver", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dx=8, align="left", font="Inter", fontSize=11, color=p["text"]).encode(
        x="Value:Q", y=alt.Y("Driver:N", sort=None), text=alt.Text("Value:Q", format=",.0f")
    )
    return (bars + text).properties(title="Impact engine", height=320)


def impact_waterfall_chart(model, p):
    df = pd.DataFrame(
        [
            ("Savings", model["savings"]),
            ("AI attach", model["ai_attach"]),
            ("Conversion uplift", model["conv_uplift"]),
            ("Faster capture", model["speed_capture"]),
            ("Process upside", model["process_uplift"]),
            ("Retention value", model["people_risk"]),
        ],
        columns=["Driver", "Value"],
    )
    df["End"] = df["Value"].cumsum()
    df["Start"] = df["End"] - df["Value"]
    df["Color"] = [p["success"], p["accent_2"], p["accent"], p["accent_3"], p["warn"], p["danger"]]
    bars = alt.Chart(df).mark_bar(cornerRadius=8).encode(
        x=alt.X("Driver:N", title=""),
        y=alt.Y("Start:Q", title="AED"),
        y2="End:Q",
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Driver", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-8, font="Inter", fontSize=11, color=p["text"]).encode(
        x="Driver:N", y="End:Q", text=alt.Text("Value:Q", format=",.0f")
    )
    return (bars + text).properties(title="Waterfall build-up", height=320)


def scenario_chart(model, p):
    df = pd.DataFrame(
        [
            {"Scenario": "Conservative", "Value": model["conservative"], "Color": p["warn"]},
            {"Scenario": "Base case", "Value": model["base"], "Color": p["accent"]},
            {"Scenario": "Aggressive", "Value": model["aggressive"], "Color": p["success"]},
        ]
    )
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=58).encode(
        x=alt.X("Scenario:N", title=""),
        y=alt.Y("Value:Q", title="Annual impact value (AED)"),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Scenario", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-10, font="Inter", fontSize=11, color=p["text"]).encode(
        x="Scenario:N", y="Value:Q", text=alt.Text("Value:Q", format=",.0f")
    )
    return (bars + text).properties(title="Scenario view", height=300)


def value_realization_chart(model, p):
    months = list(range(1, 13))
    base_curve = np.array([0.06, 0.12, 0.19, 0.28, 0.38, 0.49, 0.60, 0.70, 0.79, 0.87, 0.94, 1.00])
    cons_curve = np.array([0.04, 0.09, 0.15, 0.22, 0.31, 0.40, 0.50, 0.61, 0.71, 0.81, 0.90, 1.00])
    aggr_curve = np.array([0.08, 0.16, 0.25, 0.35, 0.46, 0.58, 0.69, 0.79, 0.87, 0.93, 0.97, 1.00])
    df = pd.DataFrame(
        {
            "Month": months,
            "Conservative": model["conservative"] * cons_curve,
            "Base case": model["base"] * base_curve,
            "Aggressive": model["aggressive"] * aggr_curve,
        }
    )
    long = df.melt("Month", var_name="Path", value_name="Value")
    chart = alt.Chart(long).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("Month:O", title="Month"),
        y=alt.Y("Value:Q", title="Cumulative value realized (AED)"),
        color=alt.Color(
            "Path:N",
            scale=alt.Scale(
                domain=["Conservative", "Base case", "Aggressive"],
                range=[p["warn"], p["accent"], p["success"]],
            ),
            title="",
        ),
        tooltip=["Month", "Path", alt.Tooltip("Value:Q", format=",.0f")],
    )
    return chart.properties(title="Value realization over 12 months", height=300)


def forecast_band_chart(model, p):
    months = list(range(1, 13))
    base_curve = np.array([0.06, 0.12, 0.19, 0.28, 0.38, 0.49, 0.60, 0.70, 0.79, 0.87, 0.94, 1.00])
    cons_curve = np.array([0.04, 0.09, 0.15, 0.22, 0.31, 0.40, 0.50, 0.61, 0.71, 0.81, 0.90, 1.00])
    aggr_curve = np.array([0.08, 0.16, 0.25, 0.35, 0.46, 0.58, 0.69, 0.79, 0.87, 0.93, 0.97, 1.00])

    band = pd.DataFrame(
        {
            "Month": months,
            "Low": model["conservative"] * cons_curve,
            "High": model["aggressive"] * aggr_curve,
            "Base": model["base"] * base_curve,
        }
    )

    area = alt.Chart(band).mark_area(opacity=0.18, color=p["accent"]).encode(
        x=alt.X("Month:O", title="Month"),
        y=alt.Y("Low:Q", title="Forecast value (AED)"),
        y2="High:Q",
        tooltip=[alt.Tooltip("Low:Q", format=",.0f"), alt.Tooltip("High:Q", format=",.0f")],
    )
    line = alt.Chart(band).mark_line(point=True, color=p["success"], strokeWidth=3).encode(
        x="Month:O",
        y="Base:Q",
        tooltip=[alt.Tooltip("Base:Q", format=",.0f")],
    )
    return (area + line).properties(title="Forecast band", height=300)


def cost_vs_return_chart(row, model, p):
    df = pd.DataFrame(
        [
            {"Metric": "Full-time executive stack", "Value": float(row["full_time_equivalent_cost_aed"]), "Type": "Cost"},
            {"Metric": "Fractional + AI solution", "Value": float(row["fractional_ai_solution_cost_aed"]), "Type": "Cost"},
            {"Metric": "Modeled impact created", "Value": model["total"], "Type": "Return"},
        ]
    )
    df["Color"] = df["Type"].map({"Cost": p["danger"], "Return": p["success"]})
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=55).encode(
        x=alt.X("Metric:N", title=""),
        y=alt.Y("Value:Q", title="AED value"),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Metric", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-10, color=p["text"], font="Inter", fontSize=11).encode(
        x="Metric:N", y="Value:Q", text=alt.Text("Value:Q", format=",.0f")
    )
    return (bars + text).properties(title="Cost of status quo vs return", height=320)


def executive_score_chart(row, model, p):
    df = pd.DataFrame(
        [
            {"Dimension": "Proof strength", "Score": model["proof"], "Color": p["success"]},
            {"Dimension": "Urgency pressure", "Score": model["urgency"], "Color": p["danger"]},
            {"Dimension": "Readiness", "Score": model["readiness"], "Color": p["accent_2"]},
            {"Dimension": "Feasibility", "Score": model["feasibility"], "Color": p["accent"]},
            {"Dimension": "Conviction", "Score": model["conviction"], "Color": p["accent_3"]},
        ]
    ).sort_values("Score", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=25).encode(
        x=alt.X("Score:Q", title="Score out of 100", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Dimension:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Dimension", alt.Tooltip("Score:Q", format=".1f")],
    )
    rule = alt.Chart(pd.DataFrame({"x": [70]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(x="x:Q")
    return (rule + bars).properties(title="Executive buying case", height=300)


def role_priority_chart(row, p):
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
        x=alt.X("Enablement:Q", title="Operating evidence / enablement", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Need:Q", title="Executive need score", scale=alt.Scale(domain=[0, 100])),
        size=alt.Size("Priority:Q", scale=alt.Scale(range=[180, 1400]), title="Priority"),
        color=alt.Color("Role:N", title=""),
        tooltip=["Role", alt.Tooltip("Need:Q", format=".1f"), alt.Tooltip("Enablement:Q", format=".1f"), alt.Tooltip("Priority:Q", format=".1f")],
    )
    labels = alt.Chart(df).mark_text(dy=-16, font="Inter", fontSize=11, color=p["text"]).encode(
        x="Enablement:Q", y="Need:Q", text="Role:N"
    )
    return (scatter + labels).properties(title="Role priority matrix", height=320)


def proof_heatmap(row):
    df = pd.DataFrame(
        [
            ("Pain", "Urgency", float(row["urgency_score"])),
            ("Pain", "Compliance risk", float(row["compliance_risk_score"])),
            ("Pain", "Backlog pressure", float(row["project_backlog_score"])),
            ("Pain", "Reporting friction", min(100, float(row["reporting_delay_days"]) * 3.2)),
            ("Capability", "Digital maturity", float(row["digital_maturity_score"])),
            ("Capability", "Data maturity", float(row["data_maturity_score"])),
            ("Capability", "Automation potential", float(row["automation_potential_score"])),
            ("Capability", "Process efficiency", float(row["process_efficiency_score"])),
            ("Commercial", "Win probability", float(row["win_probability"]) * 100),
            ("Commercial", "Response probability", float(row["response_probability"]) * 100),
            ("Commercial", "Upsell propensity", float(row["upsell_propensity_score"])),
            ("Commercial", "Account health", float(row["account_health_score"])),
        ],
        columns=["Cluster", "Metric", "Score"],
    )
    heat = alt.Chart(df).mark_rect(cornerRadius=6).encode(
        x=alt.X("Cluster:N", title=""),
        y=alt.Y("Metric:N", sort=None, title=""),
        color=alt.Color("Score:Q", scale=alt.Scale(scheme="tealblues"), title="Score"),
        tooltip=["Cluster", "Metric", alt.Tooltip("Score:Q", format=".1f")],
    )
    text = alt.Chart(df).mark_text(font="Inter", fontSize=11).encode(
        x="Cluster:N",
        y=alt.Y("Metric:N", sort=None),
        text=alt.Text("Score:Q", format=".0f"),
        color=alt.condition(alt.datum.Score > 58, alt.value("white"), alt.value("#0F172A")),
    )
    return (heat + text).properties(title="Proof map", height=360)


def before_after_chart(row, p):
    current = {
        "Decision speed": max(10, 100 - min(100, float(row["reporting_delay_days"]) * 3.0)),
        "People stability": max(5, 100 - float(row["attrition_rate_pct"]) * 2.2),
        "Execution quality": float(row["process_efficiency_score"]),
        "Commercial efficiency": min(100, float(row["lead_conversion_pct"]) * 8 + float(row["campaign_roi_x"]) * 12),
        "AI leverage": (float(row["digital_maturity_score"]) + float(row["automation_potential_score"])) / 2,
    }
    improved = {
        "Decision speed": min(100, current["Decision speed"] + 16 + float(row["data_maturity_score"]) * 0.09),
        "People stability": min(100, current["People stability"] + 10 + float(row["upsell_propensity_score"]) * 0.05),
        "Execution quality": min(100, current["Execution quality"] + 14 + float(row["automation_potential_score"]) * 0.08),
        "Commercial efficiency": min(100, current["Commercial efficiency"] + 10 + float(row["incremental_uplift_pct"]) * 1.8 + float(row["response_probability"]) * 12),
        "AI leverage": min(100, current["AI leverage"] + 12 + float(row["ai_attach_value_aed"]) / max(1, float(row["expected_annual_contract_value_aed"])) * 18),
    }
    rows = []
    for k in current:
        rows.append({"Dimension": k, "State": "Current state", "Score": current[k]})
        rows.append({"Dimension": k, "State": "Post-implementation", "Score": improved[k]})
    df = pd.DataFrame(rows)
    return alt.Chart(df).mark_bar(cornerRadius=6).encode(
        x=alt.X("Score:Q", title="Capability score", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Dimension:N", sort=None, title=""),
        xOffset="State:N",
        color=alt.Color(
            "State:N",
            scale=alt.Scale(domain=["Current state", "Post-implementation"], range=[p["danger"], p["success"]]),
            title="",
        ),
        tooltip=["Dimension", "State", alt.Tooltip("Score:Q", format=".1f")],
    ).properties(title="Before and after", height=320)


def revenue_motion_chart(row, p):
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
        x="Quarter:N", y=alt.Y("Revenue growth %:Q", title="Revenue growth %")
    )
    return alt.layer(bars, line).resolve_scale(y="independent").properties(
        title="Commercial motion",
        height=300,
    )


def funnel_chart(row, p):
    touches = max(int(row["sales_touchpoints_90d"]), 1)
    responses = max(1, int(round(touches * float(row["response_probability"]) * 0.9)))
    meetings = max(int(row["meetings_booked_90d"]), 1 if responses > 1 else 0)
    proposals = max(int(row["proposal_count_90d"]), 1 if meetings > 1 else 0)
    closes = max(0.5, float(row["win_probability"]) * max(1, proposals))
    df = pd.DataFrame(
        [
            {"Stage": "Touches", "Value": touches, "Color": p["accent_3"]},
            {"Stage": "Responses", "Value": responses, "Color": p["accent"]},
            {"Stage": "Meetings", "Value": meetings, "Color": p["accent_2"]},
            {"Stage": "Proposals", "Value": proposals, "Color": p["warn"]},
            {"Stage": "Expected closes", "Value": closes, "Color": p["success"]},
        ]
    ).sort_values("Value", ascending=False)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X("Value:Q", title="Volume / expected outcome"),
        y=alt.Y("Stage:N", sort="-x", title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Stage", alt.Tooltip("Value:Q", format=".1f")],
    )
    return bars.properties(title="Commercial conversion funnel", height=280)


def peer_map_chart(filtered, row, p):
    peers = filtered.copy()
    peers["selected"] = peers["company_name"].eq(row["company_name"])
    base = alt.Chart(peers).mark_circle(opacity=0.8, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("urgency_score:Q", title="Urgency score"),
        y=alt.Y("impact_proxy:Q", title="Impact proxy (AED)"),
        size=alt.Size("win_probability:Q", scale=alt.Scale(range=[70, 1000]), title="Win probability"),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("primary_fractional_cxo:N", title="Primary CXO")),
        tooltip=["company_name", "sector", "primary_fractional_cxo", alt.Tooltip("impact_proxy:Q", format=",.0f"), "urgency_score", "win_probability"],
    )
    label = alt.Chart(peers[peers["selected"]]).mark_text(dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]).encode(
        x="urgency_score:Q", y="impact_proxy:Q", text="company_name:N"
    )
    return (base + label).properties(title="Portfolio position", height=340)


def percentile_chart(filtered, row, p):
    metrics = [
        ("Savings", "estimated_annual_savings_aed"),
        ("ACV", "expected_annual_contract_value_aed"),
        ("Win probability", "win_probability"),
        ("ROI", "expected_roi_multiple"),
        ("Urgency", "urgency_score"),
        ("LTV", "expected_account_ltv_aed"),
    ]
    rows = []
    for label, col in metrics:
        percentile = float((filtered[col] <= row[col]).mean() * 100)
        color = p["success"] if percentile >= 75 else p["accent"] if percentile >= 50 else p["warn"]
        rows.append({"Metric": label, "Percentile": percentile, "Color": color})
    df = pd.DataFrame(rows).sort_values("Percentile", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("Percentile:Q", title="Percentile within filtered portfolio", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Metric:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Metric", alt.Tooltip("Percentile:Q", format=".1f")],
    )
    rule = alt.Chart(pd.DataFrame({"x": [50]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(x="x:Q")
    text = alt.Chart(df).mark_text(dx=8, align="left", color=p["text"], font="Inter", fontSize=11).encode(
        x="Percentile:Q", y=alt.Y("Metric:N", sort=None), text=alt.Text("Percentile:Q", format=".0f")
    )
    return (rule + bars + text).properties(title="Relative strength", height=300)


def roadmap_chart(row, p):
    close_days = int(row["expected_close_days"])
    phase1 = max(12, min(20, close_days // 2 if close_days > 2 else 12))
    phase2 = close_days
    phase3 = close_days + 30
    phase4 = max(phase3 + 25, int(row["next_service_expansion_days"]))
    df = pd.DataFrame(
        [
            {"Stage": "Diagnose pain and quantify impact", "Start": 0, "End": phase1, "Owner": "Commercial"},
            {"Stage": "Secure sponsor and sign", "Start": phase1, "End": phase2, "Owner": "Commercial"},
            {"Stage": f"Launch {row['primary_fractional_cxo']} workstream", "Start": phase2, "End": phase3, "Owner": row["primary_fractional_cxo"]},
            {"Stage": "Deploy AI reporting + agents", "Start": phase2 + 10, "End": phase3 + 18, "Owner": "AI layer"},
            {"Stage": f"Expand into {row['secondary_fractional_cxo']}", "Start": phase3, "End": phase4, "Owner": row["secondary_fractional_cxo"]},
        ]
    )
    bars = alt.Chart(df).mark_bar(cornerRadius=8, height=22).encode(
        x=alt.X("Start:Q", title="Days from today"),
        x2="End:Q",
        y=alt.Y("Stage:N", sort=None, title=""),
        color=alt.Color("Owner:N", title=""),
        tooltip=["Stage", "Owner", "Start", "End"],
    )
    rules = alt.Chart(pd.DataFrame({"x": [close_days, phase4]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(x="x:Q")
    return (rules + bars).properties(title="Implementation path", height=290)


def segment_mix_chart(filtered, p):
    df = (
        filtered.groupby("segment_name", as_index=False)
        .agg(accounts=("company_name", "count"), impact=("impact_total", "sum"))
        .sort_values("impact", ascending=False)
    )
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=54).encode(
        x=alt.X("segment_name:N", title=""),
        y=alt.Y("impact:Q", title="Total modeled impact (AED)"),
        color=alt.Color("segment_name:N", title=""),
        tooltip=["segment_name", "accounts", alt.Tooltip("impact:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-10, font="Inter", fontSize=11, color=p["text"]).encode(
        x="segment_name:N", y="impact:Q", text=alt.Text("accounts:Q", format=",.0f")
    )
    return (bars + text).properties(title="Segment contribution", height=300)


def segment_value_risk_chart(filtered):
    df = (
        filtered.groupby("segment_name", as_index=False)
        .agg(
            accounts=("company_name", "count"),
            avg_impact=("impact_total", "mean"),
            avg_ltv=("expected_account_ltv_aed", "mean"),
            avg_risk=("client_churn_risk_score", "mean"),
        )
        .copy()
    )
    return alt.Chart(df).mark_circle(opacity=0.85, stroke="white", strokeWidth=1).encode(
        x=alt.X("avg_risk:Q", title="Average churn risk"),
        y=alt.Y("avg_ltv:Q", title="Average predicted LTV (AED)"),
        size=alt.Size("accounts:Q", scale=alt.Scale(range=[450, 3000]), title="Accounts"),
        color=alt.Color("segment_name:N", title="Segment"),
        tooltip=[
            "segment_name",
            "accounts",
            alt.Tooltip("avg_impact:Q", format=",.0f", title="Avg impact"),
            alt.Tooltip("avg_ltv:Q", format=",.0f", title="Avg LTV"),
            alt.Tooltip("avg_risk:Q", format=".1f", title="Avg churn risk"),
        ],
    ).properties(title="Segment value / risk map", height=340)


def ltv_risk_chart(filtered, row, p):
    df = filtered.copy()
    df["selected"] = np.where(df["company_name"] == row["company_name"], "Selected", "Peer")
    base = alt.Chart(df).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("client_churn_risk_score:Q", title="Churn risk"),
        y=alt.Y("expected_account_ltv_aed:Q", title="Predicted LTV (AED)"),
        size=alt.Size("impact_total:Q", scale=alt.Scale(range=[80, 1200]), title="Impact"),
        color=alt.Color(
            "selected:N",
            scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent_2"], p["danger"]]),
            legend=None,
        ),
        tooltip=["company_name", "segment_name", alt.Tooltip("expected_account_ltv_aed:Q", format=",.0f"), alt.Tooltip("client_churn_risk_score:Q", format=".1f"), alt.Tooltip("impact_total:Q", format=",.0f")],
    )
    label = alt.Chart(df[df["company_name"] == row["company_name"]]).mark_text(
        dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]
    ).encode(x="client_churn_risk_score:Q", y="expected_account_ltv_aed:Q", text="company_name:N")
    return (base + label).properties(title="LTV versus churn risk", height=340)


def ltv_band_chart(filtered, p):
    df = (
        filtered.groupby("ltv_band", as_index=False)
        .agg(accounts=("company_name", "count"), ltv=("expected_account_ltv_aed", "mean"))
        .sort_values("ltv")
    )
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=56).encode(
        x=alt.X("ltv_band:N", title=""),
        y=alt.Y("ltv:Q", title="Average LTV (AED)"),
        color=alt.Color("ltv_band:N", title=""),
        tooltip=["ltv_band", "accounts", alt.Tooltip("ltv:Q", format=",.0f")],
    )
    return bars.properties(title="LTV band ladder", height=300)


def churn_quadrant_chart(filtered, row, p):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    base = alt.Chart(df).mark_circle(opacity=0.84, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("client_churn_risk_score:Q", title="Churn risk"),
        y=alt.Y("account_health_score:Q", title="Account health"),
        size=alt.Size("expected_account_ltv_aed:Q", scale=alt.Scale(range=[80, 1300]), title="LTV"),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("risk_band:N", title="Risk band")),
        tooltip=["company_name", "risk_band", alt.Tooltip("client_churn_risk_score:Q", format=".1f"), alt.Tooltip("account_health_score:Q", format=".1f"), alt.Tooltip("expected_account_ltv_aed:Q", format=",.0f")],
    )
    v_rule = alt.Chart(pd.DataFrame({"x": [65]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(x="x:Q")
    h_rule = alt.Chart(pd.DataFrame({"y": [60]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(y="y:Q")
    label = alt.Chart(df[df["selected"]]).mark_text(dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]).encode(
        x="client_churn_risk_score:Q", y="account_health_score:Q", text="company_name:N"
    )
    return (v_rule + h_rule + base + label).properties(title="Churn quadrant", height=340)


def at_risk_leaderboard_chart(filtered, p):
    df = filtered.copy()
    df["risk_value"] = df["expected_account_ltv_aed"] * df["client_churn_risk_score"] / 100.0
    top = df.sort_values("risk_value", ascending=False).head(10)
    bars = alt.Chart(top).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("risk_value:Q", title="Value at risk (AED)"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color("segment_name:N", title=""),
        tooltip=["company_name", "segment_name", alt.Tooltip("risk_value:Q", format=",.0f")],
    )
    return bars.properties(title="At-risk leaderboard", height=320)


def next_purchase_bucket_chart(filtered, p):
    df = filtered.groupby("close_horizon", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=60).encode(
        x=alt.X("close_horizon:N", title="Expected close horizon"),
        y=alt.Y("accounts:Q", title="Accounts"),
        color=alt.Color("close_horizon:N", title=""),
        tooltip=["close_horizon", "accounts"],
    ).properties(title="Next purchase buckets", height=300)


def expansion_bucket_chart(filtered, p):
    df = filtered.groupby("expansion_horizon", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=60).encode(
        x=alt.X("expansion_horizon:N", title="Expansion horizon"),
        y=alt.Y("accounts:Q", title="Accounts"),
        color=alt.Color("expansion_horizon:N", title=""),
        tooltip=["expansion_horizon", "accounts"],
    ).properties(title="Service expansion buckets", height=300)


def next_purchase_strip_chart(filtered, row, p):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    dots = alt.Chart(df).mark_circle(size=80, opacity=0.8).encode(
        x=alt.X("expected_close_days:Q", title="Expected close days"),
        y=alt.Y("segment_name:N", title=""),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("primary_fractional_cxo:N", title="Primary CXO")),
        tooltip=["company_name", "segment_name", "primary_fractional_cxo", "expected_close_days"],
    )
    return dots.properties(title="Close timing distribution", height=280)


def response_uplift_chart(filtered, row, p):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    base = alt.Chart(df).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("response_probability:Q", title="Response probability"),
        y=alt.Y("incremental_uplift_pct:Q", title="Incremental uplift %"),
        size=alt.Size("expected_annual_contract_value_aed:Q", scale=alt.Scale(range=[80, 1200]), title="ACV"),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("segment_name:N", title="Segment")),
        tooltip=["company_name", "segment_name", alt.Tooltip("response_probability:Q", format=".2f"), alt.Tooltip("incremental_uplift_pct:Q", format=".1f"), alt.Tooltip("expected_annual_contract_value_aed:Q", format=",.0f")],
    )
    label = alt.Chart(df[df["selected"]]).mark_text(dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]).encode(
        x="response_probability:Q", y="incremental_uplift_pct:Q", text="company_name:N"
    )
    return (base + label).properties(title="Market response opportunity", height=340)


def uplift_leaderboard_chart(filtered, p):
    top = (
        filtered[["company_name", "uplift_value_proxy", "segment_name"]]
        .sort_values("uplift_value_proxy", ascending=False)
        .head(12)
    )
    bars = alt.Chart(top).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("uplift_value_proxy:Q", title="Modeled uplift value (AED)"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color("segment_name:N", title=""),
        tooltip=["company_name", "segment_name", alt.Tooltip("uplift_value_proxy:Q", format=",.0f")],
    )
    return bars.properties(title="Uplift leaderboard", height=340)


def ab_test_chart(filtered):
    seg = (
        filtered.groupby("segment_name", as_index=False)
        .agg(
            response=("response_probability", "mean"),
            uplift=("incremental_uplift_pct", "mean"),
            acv=("expected_annual_contract_value_aed", "mean"),
        )
        .copy()
    )
    seg["control_conv"] = seg["response"] * 100
    seg["variant_a"] = seg["control_conv"] + seg["uplift"] * 0.65
    seg["variant_b"] = seg["control_conv"] + seg["uplift"]

    long = pd.DataFrame(
        {
            "segment_name": np.repeat(seg["segment_name"].values, 3),
            "Arm": ["Control", "Variant A", "Variant B"] * len(seg),
            "Conv": np.concatenate([seg["control_conv"], seg["variant_a"], seg["variant_b"]]),
        }
    )

    chart = alt.Chart(long).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("segment_name:N", title=""),
        y=alt.Y("Conv:Q", title="Expected conversion %"),
        color=alt.Color("Arm:N", title=""),
        xOffset="Arm:N",
        tooltip=["segment_name", "Arm", alt.Tooltip("Conv:Q", format=".2f")],
    ).properties(title="A/B test planner", height=320)
    return chart, seg


def risk_band_donut(filtered):
    df = filtered.groupby("risk_band", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return donut_chart(df, "risk_band", "accounts", "Risk band mix")


def ltv_band_donut(filtered):
    df = filtered.groupby("ltv_band", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return donut_chart(df, "ltv_band", "accounts", "LTV band mix")


def close_horizon_donut(filtered):
    df = filtered.groupby("close_horizon", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return donut_chart(df, "close_horizon", "accounts", "Close horizon mix")


def choose_geo_columns(df):
    lat_candidates = ["latitude", "lat", "hq_lat", "city_lat", "client_lat"]
    lon_candidates = ["longitude", "lon", "lng", "hq_lon", "city_lon", "client_lon"]
    place_candidates = ["city", "hq_city", "location_city", "hq_location", "location", "country", "hq_country"]
    region_candidates = ["country", "region", "city", "hq_city", "location", "hq_location"]

    lat_col = next((c for c in lat_candidates if c in df.columns), None)
    lon_col = next((c for c in lon_candidates if c in df.columns), None)
    place_col = next((c for c in place_candidates if c in df.columns), None)
    region_col = next((c for c in region_candidates if c in df.columns), None)
    return lat_col, lon_col, place_col, region_col


def geo_lookup():
    return {
        "dubai": (25.2048, 55.2708),
        "abu dhabi": (24.4539, 54.3773),
        "sharjah": (25.3463, 55.4209),
        "ajman": (25.4052, 55.5136),
        "ras al khaimah": (25.8007, 55.9762),
        "fujairah": (25.1288, 56.3265),
        "umm al quwain": (25.5647, 55.5552),
        "al ain": (24.2075, 55.7447),
        "riyadh": (24.7136, 46.6753),
        "jeddah": (21.4858, 39.1925),
        "doha": (25.2854, 51.5310),
        "muscat": (23.5880, 58.3829),
        "kuwait city": (29.3759, 47.9774),
        "manama": (26.2235, 50.5876),
        "singapore": (1.3521, 103.8198),
        "london": (51.5072, -0.1276),
        "new york": (40.7128, -74.0060),
    }


def build_map_df(filtered):
    lat_col, lon_col, place_col, region_col = choose_geo_columns(filtered)

    if lat_col and lon_col:
        df_map = filtered[[lat_col, lon_col, "company_name", "segment_name", "impact_total", "client_churn_risk_score"]].dropna().copy()
        df_map = df_map.rename(columns={lat_col: "lat", lon_col: "lon"})
        if not df_map.empty:
            return df_map, region_col

    if place_col:
        lookup = geo_lookup()
        temp = filtered[[place_col, "company_name", "segment_name", "impact_total", "client_churn_risk_score"]].copy()
        temp["place_key"] = temp[place_col].astype(str).str.strip().str.lower()
        temp["coords"] = temp["place_key"].map(lookup)
        temp = temp[temp["coords"].notna()].copy()
        if not temp.empty:
            temp["lat"] = temp["coords"].apply(lambda x: x[0])
            temp["lon"] = temp["coords"].apply(lambda x: x[1])
            return temp[["lat", "lon", "company_name", "segment_name", "impact_total", "client_churn_risk_score"]], region_col

    return None, region_col


def geo_deck(df_map):
    if df_map is None or df_map.empty:
        return None

    df_map = df_map.copy()
    max_impact = max(float(df_map["impact_total"].max()), 1.0)
    df_map["radius"] = np.clip((df_map["impact_total"] / max_impact) * 42000 + 7000, 7000, 46000)

    view_state = pdk.ViewState(
        latitude=float(df_map["lat"].mean()),
        longitude=float(df_map["lon"].mean()),
        zoom=4.3,
        pitch=35,
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        get_position="[lon, lat]",
        get_radius="radius",
        get_fill_color=[37, 99, 235, 165],
        pickable=True,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
    )

    tooltip = {
        "html": "<b>{company_name}</b><br/>Segment: {segment_name}<br/>Impact: {impact_total}<br/>Churn risk: {client_churn_risk_score}",
        "style": {"backgroundColor": "#0F172A", "color": "white"},
    }
    return pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)


def geo_summary_chart(filtered, region_col, p):
    if region_col and region_col in filtered.columns:
        df = (
            filtered.groupby(region_col, as_index=False)
            .agg(accounts=("company_name", "count"), impact=("impact_total", "sum"))
            .sort_values("impact", ascending=False)
            .head(12)
        )
        return alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
            x=alt.X("impact:Q", title="Modeled impact (AED)"),
            y=alt.Y(f"{region_col}:N", sort="-x", title=""),
            color=alt.Color(f"{region_col}:N", title=""),
            tooltip=[region_col, "accounts", alt.Tooltip("impact:Q", format=",.0f")],
        ).properties(title="Regional value distribution", height=320)

    df = (
        filtered.groupby("sector", as_index=False)
        .agg(accounts=("company_name", "count"), impact=("impact_total", "sum"))
        .sort_values("impact", ascending=False)
        .head(12)
    )
    return alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("impact:Q", title="Modeled impact (AED)"),
        y=alt.Y("sector:N", sort="-x", title=""),
        color=alt.Color("sector:N", title=""),
        tooltip=["sector", "accounts", alt.Tooltip("impact:Q", format=",.0f")],
    ).properties(title="Sector value distribution", height=320)


df = load_data()
init_state(df)

palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)
inject_css(palette)

st.markdown(
    f"""
    <div class='hero'>
        <div class='hero-wrap'>
            <div>
                <h1>Yalla CXO Impact OS</h1>
                <p>
                    A tab-heavy rebuild with far more visual coverage: executive summary, proof, metrics, segmentation, value, churn, timing,
                    forecasting, response, experimentation, geography, and comparable-account drilldown.
                </p>
            </div>
            <div class='chip'>{st.session_state.appearance_mode} mode</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Setup: company, filters, and appearance", expanded=False):
    c1, c2, c3 = st.columns([1.35, 0.55, 0.55], gap="large")
    with c1:
        options = sorted(df["company_name"].tolist())
        current = options.index(st.session_state.selected_company) if st.session_state.selected_company in options else 0
        setup_company = st.selectbox("Company to pitch", options, index=current, key="setup_selected_company")
        if setup_company != st.session_state.selected_company:
            st.session_state.selected_company = setup_company
    with c2:
        light = st.toggle("Light mode", value=st.session_state.appearance_mode == "Light")
        st.session_state.appearance_mode = "Light" if light else "Dark"
    with c3:
        if st.button("Reset all filters", use_container_width=True):
            reset_filters(df)
            st.rerun()

    f1, f2, f3, f4 = st.columns(4, gap="large")
    with f1:
        st.multiselect("Sector", sorted(df["sector"].dropna().unique()), key="flt_sector")
    with f2:
        st.multiselect("Primary CXO", sorted(df["primary_fractional_cxo"].dropna().unique()), key="flt_role")
    with f3:
        st.multiselect("Urgency tier", sorted(df["urgency_tier"].dropna().unique()), key="flt_urgency")
    with f4:
        st.multiselect("Account tier", sorted(df["account_tier"].dropna().unique()), key="flt_tier")

    f5, f6 = st.columns([1.2, 0.8], gap="large")
    with f5:
        st.slider(
            "Revenue (AED bn)",
            float(df["revenue_aed_bn"].min()),
            float(df["revenue_aed_bn"].max()),
            key="flt_revenue",
        )
    with f6:
        st.slider("Minimum win probability", 0.0, 1.0, key="flt_min_win", step=0.01)

palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)

filtered = filtered_df(df)
if filtered.empty:
    st.warning("No companies match the current filters.")
    st.stop()

filtered = add_engineered_fields(filtered)

available = sorted(filtered["company_name"].tolist())
if st.session_state.selected_company not in available:
    st.session_state.selected_company = available[0]


def _on_company_change():
    st.session_state.selected_company = st.session_state._company_sel


sel, prev_col, next_col = st.columns([6.4, 0.8, 0.8], gap="medium")
idx = available.index(st.session_state.selected_company) if st.session_state.selected_company in available else 0
with sel:
    st.selectbox(
        "Selected company",
        available,
        index=idx,
        key="_company_sel",
        label_visibility="collapsed",
        on_change=_on_company_change,
    )
with prev_col:
    if st.button("◀", use_container_width=True, disabled=idx == 0):
        st.session_state.selected_company = available[idx - 1]
        st.rerun()
with next_col:
    if st.button("▶", use_container_width=True, disabled=idx == len(available) - 1):
        st.session_state.selected_company = available[idx + 1]
        st.rerun()

row = filtered.loc[filtered["company_name"] == st.session_state.selected_company].iloc[0]
model = build_model(row, filtered)
rec = recommendations(row, model)

pills = "".join(
    [
        f"<div class='pill'>Sector · {row['sector']}</div>",
        f"<div class='pill'>Revenue band · {row['revenue_band']}</div>",
        f"<div class='pill'>Primary role · {row['primary_fractional_cxo']}</div>",
        f"<div class='pill'>Pain archetype · {row['pain_archetype']}</div>",
        f"<div class='pill'>Urgency · {row['urgency_tier']} ({row['urgency_score']:.1f})</div>",
        f"<div class='pill'>Segment · {row['segment_name']}</div>",
        f"<div class='pill'>Service package · {row['recommended_service_package']}</div>",
    ]
)

st.markdown(
    f"""
    <div class='banner'>
        <h2>{row['company_name']}</h2>
        <p>{narrative(row, model)}</p>
        <div class='pill-row'>{pills}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="medium")
with k1:
    metric_card("Impact at stake", fmt_aed(model["total"]), "Modeled value pool if the solution is implemented well.")
with k2:
    metric_card("Predicted LTV", fmt_aed(row["expected_account_ltv_aed"]), "Value anchor for the account.")
with k3:
    metric_card("Expected ROI", f"{row['expected_roi_multiple']:.2f}x", "Financial return implied by the modeled solution.")
with k4:
    metric_card("Conviction score", f"{model['conviction']:.0f}/100", "Composite of proof, urgency, and readiness.")
with k5:
    metric_card("Win probability", f"{row['win_probability']*100:.1f}%", "Likelihood the account converts into an engagement.")
with k6:
    metric_card("Impact / cost", f"{model['payback']:.1f}x", "Modeled impact divided by solution cost.")

st.markdown(
    f"<div class='callout'><strong>Executive hook:</strong> {rec['hook']} {rec['why_now']} {rec['why_solution']} {rec['proof']}</div>",
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "Executive",
        "Evidence",
        "Metrics",
        "Segmentation",
        "LTV",
        "Churn",
        "Next Purchase",
        "Forecasting",
        "Market Response",
        "A/B Testing",
        "Geography",
        "Implementation",
    ]
)

with tabs[0]:
    section_header(
        "Executive summary",
        "Dense visual overview",
        "This tab gives you the highest-level read on portfolio position, modeled economics, and expected value realization."
    )
    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(portfolio_rank_chart(filtered, row, palette), use_container_width=True)
    with b:
        st.altair_chart(peer_map_chart(filtered, row, palette), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(impact_waterfall_chart(model, palette), use_container_width=True)
    with d:
        st.altair_chart(scenario_chart(model, palette), use_container_width=True)

    e, f = st.columns(2, gap="large")
    with e:
        st.altair_chart(value_realization_chart(model, palette), use_container_width=True)
    with f:
        st.altair_chart(cost_vs_return_chart(row, model, palette), use_container_width=True)

with tabs[1]:
    section_header(
        "Problem proof",
        "Show why this account matters",
        "This tab makes the problem legible through heat, comparison, and role-fit visuals."
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(proof_heatmap(row), use_container_width=True)
    with b:
        st.altair_chart(before_after_chart(row, palette), use_container_width=True)

    c, d = st.columns([0.52, 0.48], gap="large")
    with c:
        st.altair_chart(role_priority_chart(row, palette), use_container_width=True)
    with d:
        st.altair_chart(percentile_chart(filtered, row, palette), use_container_width=True)

with tabs[2]:
    section_header(
        "Core metrics",
        "More representations of the same case",
        "This tab adds mixed chart types so the dashboard feels analytical rather than repetitive."
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(impact_stack_chart(model, palette), use_container_width=True)
    with b:
        drivers = pd.DataFrame(
            {
                "Driver": [
                    "Savings",
                    "AI attach",
                    "Conversion",
                    "Speed",
                    "Process",
                    "Retention",
                ],
                "Value": [
                    model["savings"],
                    model["ai_attach"],
                    model["conv_uplift"],
                    model["speed_capture"],
                    model["process_uplift"],
                    model["people_risk"],
                ],
            }
        )
        st.altair_chart(donut_chart(drivers, "Driver", "Value", "Driver mix"), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(revenue_motion_chart(row, palette), use_container_width=True)
    with d:
        st.altair_chart(executive_score_chart(row, model, palette), use_container_width=True)

with tabs[3]:
    section_header(
        "Customer segmentation",
        "Group the portfolio into usable plays",
        "This tab shifts from single-account persuasion to portfolio strategy."
    )
    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(segment_value_risk_chart(filtered), use_container_width=True)
    with b:
        st.altair_chart(segment_mix_chart(filtered, palette), use_container_width=True)

    seg_table = (
        filtered.groupby("segment_name", as_index=False)
        .agg(
            accounts=("company_name", "count"),
            avg_impact=("impact_total", "mean"),
            avg_ltv=("expected_account_ltv_aed", "mean"),
            avg_risk=("client_churn_risk_score", "mean"),
            avg_response=("response_probability", "mean"),
        )
        .sort_values("avg_impact", ascending=False)
    )
    seg_table["avg_impact"] = seg_table["avg_impact"].map(fmt_aed)
    seg_table["avg_ltv"] = seg_table["avg_ltv"].map(fmt_aed)
    seg_table["avg_risk"] = seg_table["avg_risk"].round(1)
    seg_table["avg_response"] = (seg_table["avg_response"] * 100).round(1).astype(str) + "%"
    st.dataframe(seg_table, use_container_width=True, hide_index=True)

with tabs[4]:
    section_header(
        "Lifetime value",
        "Value concentration and distribution",
        "This tab focuses on account worth, value concentration, and where the selected company sits in that landscape."
    )
    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(ltv_risk_chart(filtered, row, palette), use_container_width=True)
    with b:
        st.altair_chart(ltv_band_chart(filtered, palette), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(ltv_band_donut(filtered), use_container_width=True)
    with d:
        top_ltv = (
            filtered[["company_name", "expected_account_ltv_aed", "segment_name"]]
            .sort_values("expected_account_ltv_aed", ascending=False)
            .head(12)
        )
        st.altair_chart(
            alt.Chart(top_ltv).mark_bar(cornerRadiusEnd=10, height=24).encode(
                x=alt.X("expected_account_ltv_aed:Q", title="Predicted LTV (AED)"),
                y=alt.Y("company_name:N", sort="-x", title=""),
                color=alt.Color("segment_name:N", title=""),
                tooltip=["company_name", "segment_name", alt.Tooltip("expected_account_ltv_aed:Q", format=",.0f")],
            ).properties(title="Top LTV accounts", height=320),
            use_container_width=True,
        )

with tabs[5]:
    section_header(
        "Churn and retention",
        "Quantify downside, not just upside",
        "This tab is for retention risk, value at risk, and who needs intervention fastest."
    )
    a, b = st.columns([0.54, 0.46], gap="large")
    with a:
        st.altair_chart(churn_quadrant_chart(filtered, row, palette), use_container_width=True)
    with b:
        st.altair_chart(at_risk_leaderboard_chart(filtered, palette), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(risk_band_donut(filtered), use_container_width=True)
    with d:
        churn_table = filtered[["company_name", "expected_account_ltv_aed", "client_churn_risk_score", "value_at_risk", "segment_name"]].copy()
        churn_table = churn_table.sort_values("value_at_risk", ascending=False).head(12)
        churn_table["expected_account_ltv_aed"] = churn_table["expected_account_ltv_aed"].map(fmt_aed)
        churn_table["value_at_risk"] = churn_table["value_at_risk"].map(fmt_aed)
        churn_table["client_churn_risk_score"] = churn_table["client_churn_risk_score"].round(1)
        st.dataframe(churn_table, use_container_width=True, hide_index=True)

with tabs[6]:
    section_header(
        "Next purchase timing",
        "Visualize when to push",
        "This tab is about purchase windows, expansion timing, and action sequencing."
    )
    a, b = st.columns([0.58, 0.42], gap="large")
    with a:
        st.altair_chart(roadmap_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(close_horizon_donut(filtered), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(next_purchase_bucket_chart(filtered, palette), use_container_width=True)
    with d:
        st.altair_chart(expansion_bucket_chart(filtered, palette), use_container_width=True)

    st.altair_chart(next_purchase_strip_chart(filtered, row, palette), use_container_width=True)

with tabs[7]:
    section_header(
        "Sales forecasting",
        "Base, downside, and upside",
        "This tab leans into forecast curves and time-based expected value."
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(forecast_band_chart(model, palette), use_container_width=True)
    with b:
        st.altair_chart(value_realization_chart(model, palette), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(revenue_motion_chart(row, palette), use_container_width=True)
    with d:
        st.altair_chart(scenario_chart(model, palette), use_container_width=True)

with tabs[8]:
    section_header(
        "Market response",
        "Where outreach converts into value",
        "This tab connects response probability, uplift, and funnel motion."
    )
    a, b = st.columns([0.54, 0.46], gap="large")
    with a:
        st.altair_chart(response_uplift_chart(filtered, row, palette), use_container_width=True)
    with b:
        st.altair_chart(funnel_chart(row, palette), use_container_width=True)

    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(uplift_leaderboard_chart(filtered, palette), use_container_width=True)
    with d:
        st.altair_chart(peer_map_chart(filtered, row, palette), use_container_width=True)

with tabs[9]:
    section_header(
        "A/B testing",
        "Turn targeting into experimentation",
        "This tab frames uplift as something to validate, not just claim."
    )
    ab_chart, seg = ab_test_chart(filtered)
    a, b = st.columns([0.60, 0.40], gap="large")
    with a:
        st.altair_chart(ab_chart, use_container_width=True)
    with b:
        seg_out = seg.copy()
        seg_out["control_conv"] = seg_out["control_conv"].round(2).astype(str) + "%"
        seg_out["variant_a"] = seg_out["variant_a"].round(2).astype(str) + "%"
        seg_out["variant_b"] = seg_out["variant_b"].round(2).astype(str) + "%"
        seg_out["lift_a_value"] = (
            (seg["variant_a"] - seg["control_conv"]) / 100.0 * seg["acv"] * 100
        ).map(fmt_aed)
        seg_out["lift_b_value"] = (
            (seg["variant_b"] - seg["control_conv"]) / 100.0 * seg["acv"] * 100
        ).map(fmt_aed)
        st.dataframe(
            seg_out[
                ["segment_name", "control_conv", "variant_a", "variant_b", "lift_a_value", "lift_b_value"]
            ],
            use_container_width=True,
            hide_index=True,
        )

with tabs[10]:
    section_header(
        "Geography",
        "Map the portfolio if the data supports it",
        "This tab attempts lat/lon first, then city-name mapping, then falls back to ranked geography summaries."
    )
    map_df, region_col = build_map_df(filtered)
    deck = geo_deck(map_df)
    if deck:
        st.pydeck_chart(deck, use_container_width=True)
    else:
        st.info("No coordinate-ready geography columns were found in the current filtered data, so the tab is showing ranked geography summaries instead.")

    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(geo_summary_chart(filtered, region_col, palette), use_container_width=True)
    with b:
        geo_table_cols = [c for c in [region_col, "sector"] if c is not None]
        geo_table = filtered.copy()
        if region_col and region_col in geo_table.columns:
            geo_table = (
                geo_table.groupby(region_col, as_index=False)
                .agg(accounts=("company_name", "count"), impact=("impact_total", "sum"))
                .sort_values("impact", ascending=False)
            )
            geo_table["impact"] = geo_table["impact"].map(fmt_aed)
            st.dataframe(geo_table, use_container_width=True, hide_index=True)
        else:
            geo_table = (
                geo_table.groupby("sector", as_index=False)
                .agg(accounts=("company_name", "count"), impact=("impact_total", "sum"))
                .sort_values("impact", ascending=False)
            )
            geo_table["impact"] = geo_table["impact"].map(fmt_aed)
            st.dataframe(geo_table, use_container_width=True, hide_index=True)

with tabs[11]:
    section_header(
        "Implementation",
        "End with execution confidence",
        "This tab closes with actionability, economics, and comparable accounts."
    )
    a, b = st.columns([0.58, 0.42], gap="large")
    with a:
        st.altair_chart(roadmap_chart(row, palette), use_container_width=True)
    with b:
        insight_card("First move", f"Begin with {row['ideal_next_action']}. Use the initial phase to quantify the value pool, align the sponsor, and shorten the path to commitment.")
        insight_card("Contract logic", f"Expected ACV is {fmt_aed(row['expected_annual_contract_value_aed'])}, expected LTV is {fmt_aed(row['expected_account_ltv_aed'])}, and the expected contract term is {int(row['expected_contract_term_months'])} months.")
        insight_card("Implementation confidence", f"Feasibility scores at {model['feasibility']:.0f}/100, with complexity headroom of {100-float(row['expansion_complexity_score']):.0f}, data maturity of {float(row['data_maturity_score']):.0f}, and account health of {float(row['account_health_score']):.0f}.")

    st.subheader("Closest comparable accounts")
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

st.download_button(
    "Download filtered dataset",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="yalla_cxo_tabbed_dashboard_filtered.csv",
    mime="text/csv",
    use_container_width=True,
)
