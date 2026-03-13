import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO Deal Room", page_icon="📈", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def palette(mode: str):
    if mode == "Light":
        return {
            "bg": "#F5F7FB",
            "panel": "#FFFFFF",
            "panel_soft": "rgba(255,255,255,0.82)",
            "text": "#0F172A",
            "muted": "#5B6B7F",
            "border": "rgba(15,23,42,0.08)",
            "accent": "#2563EB",
            "accent2": "#14B8A6",
            "accent3": "#7C3AED",
            "success": "#10B981",
            "danger": "#F97316",
            "warn": "#F59E0B",
            "grid": "rgba(15,23,42,0.08)",
            "hero_a": "#EAF2FF",
            "hero_b": "#F8FBFF",
            "hero_c": "#EEFFFB",
            "shadow": "0 14px 40px rgba(15,23,42,0.08)",
        }
    return {
        "bg": "#0B1220",
        "panel": "#111827",
        "panel_soft": "rgba(17,24,39,0.74)",
        "text": "#E8EEF8",
        "muted": "#A8B7CA",
        "border": "rgba(148,163,184,0.16)",
        "accent": "#60A5FA",
        "accent2": "#2DD4BF",
        "accent3": "#A78BFA",
        "success": "#34D399",
        "danger": "#FB923C",
        "warn": "#FBBF24",
        "grid": "rgba(148,163,184,0.12)",
        "hero_a": "#0F172A",
        "hero_b": "#111827",
        "hero_c": "#10243B",
        "shadow": "0 18px 46px rgba(2,6,23,0.34)",
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
                        p["accent2"],
                        p["accent3"],
                        p["success"],
                        p["danger"],
                        p["warn"],
                    ]
                },
            }
        }

    try:
        alt.themes.register("deal_room_theme", theme)
    except Exception:
        pass
    alt.themes.enable("deal_room_theme")


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
                radial-gradient(circle at 10% 10%, rgba(37,99,235,0.12), transparent 24%),
                radial-gradient(circle at 88% 8%, rgba(20,184,166,0.10), transparent 22%),
                linear-gradient(180deg, {p["bg"]} 0%, {p["bg"]} 100%);
            color: {p["text"]};
        }}

        .block-container {{
            max-width: 1500px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }}

        section[data-testid="stSidebar"] {{
            border-right: 1px solid {p["border"]};
        }}

        .hero {{
            background: linear-gradient(135deg, {p["hero_a"]} 0%, {p["hero_b"]} 55%, {p["hero_c"]} 100%);
            border: 1px solid {p["border"]};
            border-radius: 28px;
            padding: 1.35rem 1.45rem;
            box-shadow: {p["shadow"]};
            margin-bottom: 1rem;
        }}

        .hero-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.15rem;
            color: {p["text"]};
            margin: 0 0 .4rem 0;
        }}

        .hero-copy {{
            color: {p["muted"]};
            line-height: 1.6;
            margin: 0;
            max-width: 1100px;
        }}

        .pill-row {{
            display: flex;
            flex-wrap: wrap;
            gap: .5rem;
            margin-top: .9rem;
        }}

        .pill {{
            display: inline-flex;
            align-items: center;
            padding: .46rem .78rem;
            border-radius: 999px;
            border: 1px solid {p["border"]};
            background: rgba(96,165,250,0.08);
            color: {p["text"]};
            font-size: .82rem;
        }}

        .stat-card {{
            background: {p["panel_soft"]};
            border: 1px solid {p["border"]};
            border-radius: 22px;
            padding: 1rem;
            box-shadow: {p["shadow"]};
            min-height: 118px;
            backdrop-filter: blur(12px);
        }}

        .stat-label {{
            font-size: .74rem;
            letter-spacing: .08em;
            text-transform: uppercase;
            color: {p["muted"]};
            margin-bottom: .32rem;
        }}

        .stat-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.52rem;
            font-weight: 700;
            color: {p["text"]};
            line-height: 1.1;
            margin-bottom: .28rem;
        }}

        .stat-sub {{
            font-size: .84rem;
            color: {p["muted"]};
            line-height: 1.5;
        }}

        .section-kicker {{
            font-size: .78rem;
            letter-spacing: .08em;
            text-transform: uppercase;
            color: {p["accent2"]};
            margin: .55rem 0 .18rem 0;
        }}

        .section-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.42rem;
            color: {p["text"]};
            margin: 0 0 .24rem 0;
        }}

        .section-copy {{
            color: {p["muted"]};
            line-height: 1.58;
            margin-bottom: .9rem;
            max-width: 1050px;
        }}

        .note-card {{
            background: {p["panel_soft"]};
            border: 1px solid {p["border"]};
            border-left: 4px solid {p["accent"]};
            border-radius: 22px;
            padding: 1rem 1.05rem;
            box-shadow: {p["shadow"]};
            margin-bottom: 1rem;
        }}

        .note-card h4 {{
            margin: 0 0 .4rem 0;
            color: {p["text"]};
            font-size: 1rem;
        }}

        .note-card p {{
            margin: 0;
            color: {p["muted"]};
            line-height: 1.55;
        }}

        .stDataFrame {{
            border-radius: 18px;
            overflow: hidden;
        }}

        [data-testid="stMetric"] {{
            background: {p["panel_soft"]};
            border: 1px solid {p["border"]};
            border-radius: 20px;
            padding: .85rem 1rem;
        }}

        .small-divider {{
            height: 1px;
            background: {p["border"]};
            margin: .3rem 0 1rem 0;
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


def clamp(v, lo=0, hi=100):
    return float(max(lo, min(hi, v)))


def section_header(kicker, title, copy):
    st.markdown(
        f"""
        <div class="section-kicker">{kicker}</div>
        <div class="section-title">{title}</div>
        <div class="section-copy">{copy}</div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label, value, sub):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def note_card(title, body):
    st.markdown(
        f"""
        <div class="note-card">
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


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


def apply_filters(df):
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


def enrich(df):
    x = df.copy()

    conv_uplift = (
        x["recommended_acv_aed"]
        * x["baseline_conversion_probability"]
        * (x["incremental_uplift_pct"] / 100.0)
    )
    speed_capture = x["forecast_2q_revenue_aed"] * np.minimum(
        0.34, x["win_probability"] * 0.55
    )
    process_uplift = (
        x["estimated_annual_savings_aed"] * (x["automation_potential_score"] / 100.0) * 0.18
    )
    people_risk = (
        x["expected_account_ltv_aed"] * (x["client_churn_risk_score"] / 100.0) * 0.08
    )

    x["impact_proxy"] = (
        x["estimated_annual_savings_aed"]
        + x["ai_attach_value_aed"]
        + conv_uplift
        + speed_capture
        + process_uplift
        + people_risk
    )

    x["proof_proxy"] = (
        x["estimated_annual_savings_aed"].rank(pct=True) * 40
        + x["expected_roi_multiple"].rank(pct=True) * 35
        + x["win_probability"].rank(pct=True) * 25
    )

    x["urgency_proxy"] = (
        0.35 * x["urgency_score"]
        + 0.20 * x["cash_flow_volatility_score"]
        + 0.15 * x["compliance_risk_score"]
        + 0.15 * x["project_backlog_score"]
        + 0.15 * (100 - x["on_time_delivery_pct"])
    )

    x["readiness_proxy"] = (
        0.28 * x["digital_maturity_score"]
        + 0.22 * x["data_maturity_score"]
        + 0.20 * x["account_health_score"]
        + 0.15 * x["cross_sell_readiness_score"]
        + 0.15 * (x["response_probability"] * 100)
    )

    x["feasibility_proxy"] = (
        0.34 * (100 - x["expansion_complexity_score"])
        + 0.22 * x["data_maturity_score"]
        + 0.22 * x["account_health_score"]
        + 0.22 * (x["response_probability"] * 100)
    )

    x["conviction_proxy"] = (
        0.34 * x["proof_proxy"] + 0.33 * x["urgency_proxy"] + 0.33 * x["readiness_proxy"]
    )

    for c in [
        "proof_proxy",
        "urgency_proxy",
        "readiness_proxy",
        "feasibility_proxy",
        "conviction_proxy",
    ]:
        x[c] = x[c].clip(0, 100)

    x["impact_rank"] = x["impact_proxy"].rank(ascending=False, method="min")
    x["conviction_rank"] = x["conviction_proxy"].rank(ascending=False, method="min")

    return x


def build_model(row, filtered):
    total = float(row["impact_proxy"])
    conservative = total * 0.78
    aggressive = total * 1.24
    payback = total / max(float(row["fractional_ai_solution_cost_aed"]), 1.0)
    impact_rank = int(filtered.loc[row.name, "impact_rank"])
    conviction_rank = int(filtered.loc[row.name, "conviction_rank"])

    return {
        "total": total,
        "conservative": conservative,
        "base": total,
        "aggressive": aggressive,
        "proof": float(row["proof_proxy"]),
        "urgency": float(row["urgency_proxy"]),
        "readiness": float(row["readiness_proxy"]),
        "feasibility": float(row["feasibility_proxy"]),
        "conviction": float(row["conviction_proxy"]),
        "payback": payback,
        "impact_rank": impact_rank,
        "conviction_rank": conviction_rank,
    }


def narrative(row, model, filtered):
    median_impact = filtered["impact_proxy"].median()
    rank_text = f"top {int(np.ceil(model['impact_rank'] / max(len(filtered), 1) * 100))}% account"
    gap = model["total"] - median_impact
    direction = "above" if gap >= 0 else "below"
    return (
        f"{row['company_name']} is a {row['primary_fractional_cxo']}-led wedge with "
        f"{fmt_aed(model['total'])} in modeled value at stake. It sits as a {rank_text} by impact "
        f"and screens {fmt_aed(abs(gap))} {direction} the filtered portfolio median, which makes this feel like "
        f"an action case rather than a general relationship account."
    )


def role_frame(row):
    df = pd.DataFrame(
        [
            {
                "Role": "CFO",
                "Need": float(row["cfo_need_score"]),
                "Enablement": (float(row["data_maturity_score"]) + float(row["cash_flow_volatility_score"])) / 2,
            },
            {
                "Role": "CTO",
                "Need": float(row["cto_need_score"]),
                "Enablement": (float(row["digital_maturity_score"]) + float(row["cyber_risk_score"])) / 2,
            },
            {
                "Role": "CHRO",
                "Need": float(row["chro_need_score"]),
                "Enablement": (100 - float(row["attrition_rate_pct"]) * 2 + float(row["hiring_velocity_score"])) / 2,
            },
            {
                "Role": "CMO",
                "Need": float(row["cmo_need_score"]),
                "Enablement": min(100, float(row["campaign_roi_x"]) * 22 + float(row["lead_conversion_pct"]) * 4),
            },
            {
                "Role": "COO",
                "Need": float(row["coo_need_score"]),
                "Enablement": (float(row["process_efficiency_score"]) + float(row["project_backlog_score"])) / 2,
            },
        ]
    )
    df["Enablement"] = df["Enablement"].clip(0, 100)
    df["Priority"] = 0.7 * df["Need"] + 0.3 * df["Enablement"]
    return df


def benchmark_frame(filtered, row):
    metrics = [
        ("Savings", "estimated_annual_savings_aed"),
        ("ACV", "expected_annual_contract_value_aed"),
        ("ROI", "expected_roi_multiple"),
        ("Urgency", "urgency_score"),
        ("Win probability", "win_probability"),
        ("LTV", "expected_account_ltv_aed"),
    ]
    rows = []
    for label, col in metrics:
        pct = float((filtered[col] <= row[col]).mean() * 100)
        rows.append({"Metric": label, "Percentile": pct})
    out = pd.DataFrame(rows)
    out["Color"] = np.where(
        out["Percentile"] >= 75,
        "Top quartile",
        np.where(out["Percentile"] >= 50, "Above median", "Below median"),
    )
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
    subset = subset[subset["company_name"] != row["company_name"]].sort_values("distance").head(6)
    out = subset[
        [
            "company_name",
            "sector",
            "primary_fractional_cxo",
            "estimated_annual_savings_aed",
            "expected_annual_contract_value_aed",
            "win_probability",
        ]
    ].copy()
    out["estimated_annual_savings_aed"] = out["estimated_annual_savings_aed"].map(fmt_aed)
    out["expected_annual_contract_value_aed"] = out["expected_annual_contract_value_aed"].map(fmt_aed)
    out["win_probability"] = (out["win_probability"] * 100).round(1).astype(str) + "%"
    return out.rename(
        columns={
            "company_name": "Comparable company",
            "sector": "Sector",
            "primary_fractional_cxo": "Primary CXO",
            "estimated_annual_savings_aed": "Savings",
            "expected_annual_contract_value_aed": "Expected ACV",
            "win_probability": "Win probability",
        }
    )


def leaderboard_chart(filtered, selected_company, p):
    top = (
        filtered[["company_name", "sector", "impact_proxy"]]
        .sort_values("impact_proxy", ascending=False)
        .head(12)
        .copy()
    )
    top["selected"] = np.where(top["company_name"] == selected_company, "Selected", "Peer")

    bars = alt.Chart(top).mark_bar(cornerRadiusEnd=10, height=22).encode(
        x=alt.X("impact_proxy:Q", title="Modeled impact (AED)"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color(
            "selected:N",
            scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent"], p["danger"]]),
            title="",
        ),
        tooltip=["company_name", "sector", alt.Tooltip("impact_proxy:Q", format=",.0f")],
    )

    text = alt.Chart(top).mark_text(
        dx=8, align="left", color=p["text"], font="Inter", fontSize=11
    ).encode(
        x="impact_proxy:Q",
        y=alt.Y("company_name:N", sort="-x"),
        text=alt.Text("impact_proxy:Q", format=",.0f"),
    )

    return (bars + text).properties(title="Top accounts by modeled impact", height=340)


def impact_mix_chart(row, p):
    conv_uplift = (
        float(row["recommended_acv_aed"])
        * float(row["baseline_conversion_probability"])
        * (float(row["incremental_uplift_pct"]) / 100.0)
    )
    speed_capture = float(row["forecast_2q_revenue_aed"]) * min(
        0.34, float(row["win_probability"]) * 0.55
    )
    process_uplift = (
        float(row["estimated_annual_savings_aed"])
        * (float(row["automation_potential_score"]) / 100.0)
        * 0.18
    )
    people_risk = (
        float(row["expected_account_ltv_aed"])
        * (float(row["client_churn_risk_score"]) / 100.0)
        * 0.08
    )

    df = pd.DataFrame(
        [
            {"Driver": "Annual savings", "Value": float(row["estimated_annual_savings_aed"]), "Color": p["success"]},
            {"Driver": "AI attach", "Value": float(row["ai_attach_value_aed"]), "Color": p["accent2"]},
            {"Driver": "Conversion uplift", "Value": conv_uplift, "Color": p["accent"]},
            {"Driver": "Faster capture", "Value": speed_capture, "Color": p["accent3"]},
            {"Driver": "Process upside", "Value": process_uplift, "Color": p["warn"]},
            {"Driver": "Retention risk avoided", "Value": people_risk, "Color": p["danger"]},
        ]
    ).sort_values("Value", ascending=True)

    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=28).encode(
        x=alt.X("Value:Q", title="Value contribution (AED)"),
        y=alt.Y("Driver:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Driver", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(
        dx=8, align="left", font="Inter", fontSize=11, color=p["text"]
    ).encode(
        x="Value:Q",
        y=alt.Y("Driver:N", sort=None),
        text=alt.Text("Value:Q", format=",.0f"),
    )
    return (bars + text).properties(title="Where the money comes from", height=320)


def scenario_chart(model, row, p):
    df = pd.DataFrame(
        [
            {"Scenario": "Conservative", "Impact": model["conservative"], "Type": "Impact"},
            {"Scenario": "Base case", "Impact": model["base"], "Type": "Impact"},
            {"Scenario": "Aggressive", "Impact": model["aggressive"], "Type": "Impact"},
            {"Scenario": "Solution cost", "Impact": float(row["fractional_ai_solution_cost_aed"]), "Type": "Cost"},
        ]
    )
    color_scale = alt.Scale(
        domain=["Conservative", "Base case", "Aggressive", "Solution cost"],
        range=[p["warn"], p["accent"], p["success"], p["danger"]],
    )
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=56).encode(
        x=alt.X("Scenario:N", title=""),
        y=alt.Y("Impact:Q", title="AED"),
        color=alt.Color("Scenario:N", scale=color_scale, legend=None),
        tooltip=["Scenario", alt.Tooltip("Impact:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(
        dy=-10, font="Inter", fontSize=11, color=p["text"]
    ).encode(
        x="Scenario:N", y="Impact:Q", text=alt.Text("Impact:Q", format=",.0f")
    )
    return (chart + text).properties(title="Impact range versus delivery cost", height=320)


def benchmark_chart(bench, p):
    color_scale = alt.Scale(
        domain=["Below median", "Above median", "Top quartile"],
        range=[p["warn"], p["accent"], p["success"]],
    )
    bars = alt.Chart(bench).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X("Percentile:Q", title="Percentile within filtered set", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Metric:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=color_scale, title=""),
        tooltip=["Metric", alt.Tooltip("Percentile:Q", format=".1f")],
    )
    rule = alt.Chart(pd.DataFrame({"x": [50]})).mark_rule(
        strokeDash=[6, 6], color=p["grid"]
    ).encode(x="x:Q")
    text = alt.Chart(bench).mark_text(
        dx=8, align="left", font="Inter", fontSize=11, color=p["text"]
    ).encode(
        x="Percentile:Q",
        y=alt.Y("Metric:N", sort=None),
        text=alt.Text("Percentile:Q", format=".0f"),
    )
    return (rule + bars + text).properties(title="How this account compares", height=280)


def conviction_chart(model, p):
    df = pd.DataFrame(
        [
            {"Dimension": "Proof", "Score": model["proof"], "Color": p["success"]},
            {"Dimension": "Urgency", "Score": model["urgency"], "Color": p["danger"]},
            {"Dimension": "Readiness", "Score": model["readiness"], "Color": p["accent2"]},
            {"Dimension": "Feasibility", "Score": model["feasibility"], "Color": p["accent"]},
            {"Dimension": "Conviction", "Score": model["conviction"], "Color": p["accent3"]},
        ]
    ).sort_values("Score", ascending=True)

    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=25).encode(
        x=alt.X("Score:Q", title="Score / 100", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Dimension:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Dimension", alt.Tooltip("Score:Q", format=".1f")],
    )
    rule = alt.Chart(pd.DataFrame({"x": [70]})).mark_rule(
        strokeDash=[6, 6], color=p["grid"]
    ).encode(x="x:Q")
    return (rule + bars).properties(title="Should we lean in?", height=280)


def role_priority_chart(row, p):
    df = role_frame(row)
    scatter = alt.Chart(df).mark_circle(
        opacity=0.88, stroke="white", strokeWidth=1
    ).encode(
        x=alt.X("Enablement:Q", title="Enablement", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Need:Q", title="Need", scale=alt.Scale(domain=[0, 100])),
        size=alt.Size("Priority:Q", scale=alt.Scale(range=[200, 1400]), title="Priority"),
        color=alt.Color("Role:N", title=""),
        tooltip=[
            "Role",
            alt.Tooltip("Need:Q", format=".1f"),
            alt.Tooltip("Enablement:Q", format=".1f"),
            alt.Tooltip("Priority:Q", format=".1f"),
        ],
    )
    labels = alt.Chart(df).mark_text(
        dy=-16, font="Inter", fontSize=11, color=p["text"]
    ).encode(
        x="Enablement:Q", y="Need:Q", text="Role:N"
    )
    return (scatter + labels).properties(title="Where the wedge should start", height=320)


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
    return (heat + text).properties(title="Proof map", height=340)


def momentum_chart(row, p):
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

    bars = alt.Chart(df).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8,
        size=42,
        opacity=0.78,
        color=p["accent"],
    ).encode(
        x=alt.X("Quarter:N", title=""),
        y=alt.Y("Pipeline inquiries:Q", title="Pipeline inquiries"),
        tooltip=["Quarter", "Pipeline inquiries", alt.Tooltip("Revenue growth %:Q", format=".1f")],
    )

    line = alt.Chart(df).mark_line(
        point=True, strokeWidth=3, color=p["success"]
    ).encode(
        x="Quarter:N",
        y=alt.Y("Revenue growth %:Q", title="Revenue growth %"),
    )

    return alt.layer(bars, line).resolve_scale(y="independent").properties(
        title="Commercial motion",
        height=300,
    )


def peers_chart(filtered, row, p):
    peers = filtered.copy()
    peers["selected"] = np.where(peers["company_name"] == row["company_name"], "Selected", "Peer")
    base = alt.Chart(peers).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("urgency_score:Q", title="Urgency"),
        y=alt.Y("impact_proxy:Q", title="Modeled impact (AED)"),
        size=alt.Size("win_probability:Q", scale=alt.Scale(range=[80, 1000]), title="Win probability"),
        color=alt.Color(
            "selected:N",
            scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent2"], p["danger"]]),
            title="",
        ),
        tooltip=[
            "company_name",
            "sector",
            "primary_fractional_cxo",
            alt.Tooltip("impact_proxy:Q", format=",.0f"),
            alt.Tooltip("win_probability:Q", format=".2f"),
        ],
    )
    label = alt.Chart(peers[peers["company_name"] == row["company_name"]]).mark_text(
        dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]
    ).encode(
        x="urgency_score:Q",
        y="impact_proxy:Q",
        text="company_name:N",
    )
    return (base + label).properties(title="Position versus peers", height=340)


def roadmap_chart(row, p):
    close_days = int(row["expected_close_days"])
    phase1 = max(12, min(20, close_days // 2 if close_days > 2 else 12))
    phase2 = close_days
    phase3 = close_days + 30
    phase4 = max(phase3 + 25, int(row["next_service_expansion_days"]))

    df = pd.DataFrame(
        [
            {"Stage": "Quantify pain + build sponsor case", "Start": 0, "End": phase1, "Owner": "Commercial"},
            {"Stage": "Convert and sign", "Start": phase1, "End": phase2, "Owner": "Commercial"},
            {"Stage": f"Launch {row['primary_fractional_cxo']} workstream", "Start": phase2, "End": phase3, "Owner": row["primary_fractional_cxo"]},
            {"Stage": "Deploy AI reporting layer", "Start": phase2 + 10, "End": phase3 + 18, "Owner": "AI layer"},
            {"Stage": f"Expand into {row['secondary_fractional_cxo']}", "Start": phase3, "End": phase4, "Owner": row["secondary_fractional_cxo"]},
        ]
    )

    bars = alt.Chart(df).mark_bar(cornerRadius=8, height=22).encode(
        x=alt.X("Start:Q", title="Days from now"),
        x2="End:Q",
        y=alt.Y("Stage:N", sort=None, title=""),
        color=alt.Color("Owner:N", title=""),
        tooltip=["Stage", "Owner", "Start", "End"],
    )

    rules = alt.Chart(pd.DataFrame({"x": [close_days, phase4]})).mark_rule(
        strokeDash=[6, 6], color=p["grid"]
    ).encode(x="x:Q")

    return (rules + bars).properties(title="Land, prove, expand", height=290)


df = load_data()
init_state(df)

with st.sidebar:
    st.subheader("Control room")
    light = st.toggle("Light mode", value=st.session_state.appearance_mode == "Light")
    st.session_state.appearance_mode = "Light" if light else "Dark"

    if st.button("Reset filters", use_container_width=True):
        reset_filters(df)
        st.rerun()

    st.markdown("<div class='small-divider'></div>", unsafe_allow_html=True)

    st.caption("Filter the portfolio")
    st.multiselect("Sector", sorted(df["sector"].dropna().unique()), key="flt_sector")
    st.multiselect("Primary CXO", sorted(df["primary_fractional_cxo"].dropna().unique()), key="flt_role")
    st.multiselect("Urgency tier", sorted(df["urgency_tier"].dropna().unique()), key="flt_urgency")
    st.multiselect("Account tier", sorted(df["account_tier"].dropna().unique()), key="flt_tier")
    st.slider(
        "Revenue (AED bn)",
        float(df["revenue_aed_bn"].min()),
        float(df["revenue_aed_bn"].max()),
        key="flt_revenue",
    )
    st.slider("Minimum win probability", 0.0, 1.0, key="flt_min_win", step=0.01)

p = palette(st.session_state.appearance_mode)
enable_altair_theme(p)
inject_css(p)

filtered = enrich(apply_filters(df))
if filtered.empty:
    st.warning("No companies match the current filters.")
    st.stop()

companies = sorted(filtered["company_name"].tolist())
if st.session_state.selected_company not in companies:
    st.session_state.selected_company = companies[0]

top_a, top_b, top_c = st.columns([3.5, 1.2, 1.2], gap="medium")
with top_a:
    selected_company = st.selectbox("Selected account", companies, index=companies.index(st.session_state.selected_company))
    st.session_state.selected_company = selected_company
with top_b:
    st.metric("Accounts in view", len(filtered))
with top_c:
    st.metric("Portfolio impact", fmt_aed(filtered["impact_proxy"].sum()))

row = filtered.loc[filtered["company_name"] == st.session_state.selected_company].iloc[0]
model = build_model(row, filtered)
bench = benchmark_frame(filtered, row)

badges = "".join(
    [
        f"<span class='pill'>Sector · {row['sector']}</span>",
        f"<span class='pill'>Revenue band · {row['revenue_band']}</span>",
        f"<span class='pill'>Primary wedge · {row['primary_fractional_cxo']}</span>",
        f"<span class='pill'>Pain · {row['pain_archetype']}</span>",
        f"<span class='pill'>Urgency · {row['urgency_tier']} ({row['urgency_score']:.0f})</span>",
        f"<span class='pill'>Package · {row['recommended_service_package']}</span>",
    ]
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">{row['company_name']}</div>
        <p class="hero-copy">{narrative(row, model, filtered)}</p>
        <div class="pill-row">{badges}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5, m6 = st.columns(6, gap="medium")
with m1:
    stat_card("Impact at stake", fmt_aed(model["total"]), "Modeled value pool if we execute well.")
with m2:
    stat_card("Conviction", f"{model['conviction']:.0f}/100", f"Rank #{model['conviction_rank']} on conviction.")
with m3:
    stat_card("Portfolio rank", f"#{model['impact_rank']}/{len(filtered)}", "Based on modeled impact versus filtered peers.")
with m4:
    stat_card("Expected ROI", f"{float(row['expected_roi_multiple']):.2f}x", "Financial return implied by the account profile.")
with m5:
    stat_card("Win probability", f"{float(row['win_probability']) * 100:.1f}%", f"Expected close window: {int(row['expected_close_days'])} days.")
with m6:
    stat_card("Impact / cost", f"{model['payback']:.1f}x", "Modeled impact divided by solution delivery cost.")

section_header(
    "Portfolio context",
    "Start with where this account sits",
    "This makes the reader decide if the company is merely interesting or genuinely worth prioritizing before they get into the detail.",
)

c1, c2 = st.columns([0.55, 0.45], gap="large")
with c1:
    st.altair_chart(leaderboard_chart(filtered, row["company_name"], p), use_container_width=True)
with c2:
    st.altair_chart(peers_chart(filtered, row, p), use_container_width=True)
    st.altair_chart(benchmark_chart(bench, p), use_container_width=True)

section_header(
    "Value architecture",
    "Show the economic case in one glance",
    "The page should make it obvious where the value comes from, what range is realistic, and whether the economics justify action now.",
)

c3, c4 = st.columns([0.56, 0.44], gap="large")
with c3:
    st.altair_chart(impact_mix_chart(row, p), use_container_width=True)
with c4:
    st.altair_chart(scenario_chart(model, row, p), use_container_width=True)
    note_card(
        "Pitch hook",
        f"{row['company_name']} should be sold as an impact case, not a staffing case. The core wedge is {row['primary_fractional_cxo']}, and the buyer can justify action against {fmt_aed(float(row['full_time_equivalent_cost_aed']))} in full-time executive cost and slower execution.",
    )
    note_card(
        "Expansion logic",
        f"Land with {row['primary_fractional_cxo']}, use AI-supported roles ({row['ai_supported_roles']}) plus addons like {row['ai_agent_addons']}, then expand into {row['secondary_fractional_cxo']} in roughly {int(row['next_service_expansion_days'])} days.",
    )

section_header(
    "Why now",
    "Make the problem undeniable",
    "This section turns the data into proof: pain pressure, operating evidence, wedge fit, and whether the commercial motion suggests a deal that can actually move.",
)

c5, c6 = st.columns([0.52, 0.48], gap="large")
with c5:
    st.altair_chart(proof_heatmap(row), use_container_width=True)
    st.altair_chart(momentum_chart(row, p), use_container_width=True)
with c6:
    st.altair_chart(conviction_chart(model, p), use_container_width=True)
    st.altair_chart(role_priority_chart(row, p), use_container_width=True)

section_header(
    "Action plan",
    "End with a credible path to execution",
    "The last screen should remove ambiguity: what to do first, how the motion unfolds, and which similar accounts validate the shape of the opportunity.",
)

c7, c8 = st.columns([0.58, 0.42], gap="large")
with c7:
    st.altair_chart(roadmap_chart(row, p), use_container_width=True)
with c8:
    note_card(
        "First move",
        f"Begin with: {row['ideal_next_action']}. Use the first phase to quantify the value pool, align the sponsor, and compress the path to commitment.",
    )
    note_card(
        "Commercial structure",
        f"Expected ACV is {fmt_aed(float(row['expected_annual_contract_value_aed']))}, expected LTV is {fmt_aed(float(row['expected_account_ltv_aed']))}, and expected contract term is {int(row['expected_contract_term_months'])} months.",
    )
    note_card(
        "Delivery confidence",
        f"Feasibility is {model['feasibility']:.0f}/100. Complexity headroom is {100 - float(row['expansion_complexity_score']):.0f}, data maturity is {float(row['data_maturity_score']):.0f}, and account health is {float(row['account_health_score']):.0f}.",
    )

st.subheader("Closest comparable accounts")
st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

st.download_button(
    "Download filtered dataset",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="yalla_cxo_deal_room_filtered.csv",
    mime="text/csv",
    use_container_width=True,
)
