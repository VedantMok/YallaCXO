import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import pydeck as pdk

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

st.set_page_config(page_title="Yalla Growth Analytics Studio", page_icon="🧠", layout="wide")


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
            "bg2": "#ECF3FF",
            "panel": "rgba(255,255,255,0.88)",
            "panel_solid": "#FFFFFF",
            "border": "rgba(15,23,42,0.08)",
            "text": "#0F172A",
            "muted": "#5B6B7F",
            "accent": "#2563EB",
            "accent2": "#14B8A6",
            "accent3": "#7C3AED",
            "success": "#10B981",
            "danger": "#F97316",
            "warn": "#F59E0B",
            "grid": "rgba(15,23,42,0.08)",
            "hero1": "#EAF2FF",
            "hero2": "#F8FBFF",
            "hero3": "#EEFFFB",
            "shadow": "0 16px 42px rgba(15,23,42,0.08)",
            "chip": "rgba(37,99,235,0.08)",
        }
    return {
        "bg": "#0B1220",
        "bg2": "#111827",
        "panel": "rgba(15,23,42,0.74)",
        "panel_solid": "#111827",
        "border": "rgba(148,163,184,0.14)",
        "text": "#E8EEF8",
        "muted": "#A8B7CA",
        "accent": "#60A5FA",
        "accent2": "#2DD4BF",
        "accent3": "#A78BFA",
        "success": "#34D399",
        "danger": "#FB923C",
        "warn": "#FBBF24",
        "grid": "rgba(148,163,184,0.12)",
        "hero1": "#0F172A",
        "hero2": "#111827",
        "hero3": "#10243B",
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
        alt.themes.register("growth_studio_theme", theme)
    except Exception:
        pass
    alt.themes.enable("growth_studio_theme")


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
                radial-gradient(circle at 8% 12%, rgba(37,99,235,0.12), transparent 26%),
                radial-gradient(circle at 92% 8%, rgba(20,184,166,0.10), transparent 22%),
                linear-gradient(180deg, {p["bg"]} 0%, {p["bg"]} 100%);
            color: {p["text"]};
        }}

        .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}

        .hero {{
            background: linear-gradient(135deg, {p["hero1"]} 0%, {p["hero2"]} 55%, {p["hero3"]} 100%);
            border: 1px solid {p["border"]};
            border-radius: 30px;
            padding: 1.4rem 1.5rem;
            box-shadow: {p["shadow"]};
            margin-bottom: 1rem;
        }}

        .hero-title {{
            font-family: 'Space Grotesk', sans-serif;
            margin: 0;
            color: {p["text"]};
            font-size: 2.25rem;
        }}

        .hero-copy {{
            margin: .45rem 0 0 0;
            color: {p["muted"]};
            line-height: 1.65;
            max-width: 1050px;
        }}

        .pill-row {{
            display: flex;
            gap: .55rem;
            flex-wrap: wrap;
            margin-top: .9rem;
        }}

        .pill {{
            display: inline-flex;
            padding: .48rem .78rem;
            border-radius: 999px;
            background: {p["chip"]};
            border: 1px solid {p["border"]};
            color: {p["text"]};
            font-size: .82rem;
        }}

        .metric {{
            background: {p["panel"]};
            border: 1px solid {p["border"]};
            border-radius: 22px;
            padding: 1rem .96rem;
            min-height: 122px;
            box-shadow: {p["shadow"]};
            backdrop-filter: blur(12px);
        }}

        .metric .label {{
            font-size: .74rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            color: {p["muted"]};
            margin-bottom: .32rem;
        }}

        .metric .value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.48rem;
            font-weight: 700;
            color: {p["text"]};
            line-height: 1.1;
            margin-bottom: .25rem;
        }}

        .metric .sub {{
            font-size: .84rem;
            color: {p["muted"]};
            line-height: 1.45;
        }}

        .section-kicker {{
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            color: {p["accent2"]};
            margin-bottom: .26rem;
        }}

        .section-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.36rem;
            color: {p["text"]};
            margin: .06rem 0 .18rem 0;
        }}

        .section-copy {{
            color: {p["muted"]};
            line-height: 1.58;
            margin-bottom: .95rem;
            max-width: 1040px;
        }}

        .insight {{
            background: {p["panel"]};
            border: 1px solid {p["border"]};
            border-left: 4px solid {p["accent"]};
            border-radius: 18px;
            padding: 1rem 1.02rem;
            box-shadow: {p["shadow"]};
            height: 100%;
        }}

        .insight h4 {{
            margin: 0 0 .42rem 0;
            color: {p["text"]};
            font-size: 1rem;
        }}

        .insight p {{
            margin: 0;
            color: {p["muted"]};
            line-height: 1.56;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: .45rem;
            margin-bottom: .35rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: {p["panel"]};
            border: 1px solid {p["border"]};
            border-radius: 14px;
            color: {p["muted"]};
            padding: .55rem .95rem;
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(180deg, rgba(37,99,235,0.12), rgba(20,184,166,0.12));
            color: {p["text"]};
            border-color: {p["accent"]};
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            background: {p["panel"]};
            border-color: {p["border"]};
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {p["border"]};
            border-radius: 18px;
            overflow: hidden;
        }}

        section[data-testid="stSidebar"] {{
            background: {p["bg2"]};
            border-right: 1px solid {p["border"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Utils
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


def safe_pct(s):
    return (s * 100).clip(0, 100)


def choose_geo_columns(df):
    lat_candidates = ["latitude", "lat", "city_lat", "hq_lat", "client_lat"]
    lon_candidates = ["longitude", "lon", "lng", "city_lon", "hq_lon", "client_lon"]
    lat = next((c for c in lat_candidates if c in df.columns), None)
    lon = next((c for c in lon_candidates if c in df.columns), None)
    return lat, lon


# -----------------------------
# State / filters
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
        & df["revenue_aed_bn"].between(st.session_state.flt_revenue[0], st.session_state.flt_revenue[1])
        & (df["win_probability"] >= st.session_state.flt_min_win)
    ].copy()


# -----------------------------
# Feature engineering
# -----------------------------
def zscore_pct(series, value):
    s = pd.Series(series).astype(float)
    std = float(s.std())
    if std == 0 or np.isnan(std):
        return 50.0
    z = (float(value) - float(s.mean())) / std
    return float(max(0, min(100, 50 + 18 * z)))


def build_model(row, filtered):
    savings = float(row["estimated_annual_savings_aed"])
    ai_attach = float(row["ai_attach_value_aed"])
    conv_uplift = float(row["recommended_acv_aed"]) * float(row["baseline_conversion_probability"]) * (
        float(row["incremental_uplift_pct"]) / 100.0
    )
    speed_capture = float(row["forecast_2q_revenue_aed"]) * min(0.34, float(row["win_probability"]) * 0.55)
    process_uplift = savings * (float(row["automation_potential_score"]) / 100.0) * 0.18
    people_risk = float(row["expected_account_ltv_aed"]) * (float(row["client_churn_risk_score"]) / 100.0) * 0.08
    total = savings + ai_attach + conv_uplift + speed_capture + process_uplift + people_risk

    proof = (
        0.34 * zscore_pct(filtered["estimated_annual_savings_aed"], row["estimated_annual_savings_aed"])
        + 0.33 * zscore_pct(filtered["expected_roi_multiple"], row["expected_roi_multiple"])
        + 0.33 * zscore_pct(filtered["win_probability"], row["win_probability"])
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
        "proof": float(np.clip(proof, 0, 100)),
        "urgency": float(np.clip(urgency, 0, 100)),
        "readiness": float(np.clip(readiness, 0, 100)),
        "feasibility": float(np.clip(feasibility, 0, 100)),
        "conviction": float(np.clip(conviction, 0, 100)),
        "conservative": conservative,
        "base": total,
        "aggressive": aggressive,
        "payback": payback,
    }


def add_engineered_fields(df):
    out = df.copy()

    models = []
    for idx, row in out.iterrows():
        m = build_model(row, out)
        models.append(
            {
                "impact_total": m["total"],
                "impact_conservative": m["conservative"],
                "impact_base": m["base"],
                "impact_aggressive": m["aggressive"],
                "proof_score": m["proof"],
                "urgency_score_model": m["urgency"],
                "readiness_score": m["readiness"],
                "feasibility_score": m["feasibility"],
                "conviction_score": m["conviction"],
                "impact_payback": m["payback"],
            }
        )
    model_df = pd.DataFrame(models, index=out.index)
    out = pd.concat([out, model_df], axis=1)

    out["ltv_band"] = pd.qcut(
        out["expected_account_ltv_aed"].rank(method="first"),
        4,
        labels=["Low", "Mid", "High", "Elite"],
    )

    out["close_horizon"] = pd.cut(
        out["expected_close_days"],
        bins=[-1, 30, 60, 120, 9999],
        labels=["0-30d", "31-60d", "61-120d", "120d+"],
    )

    out["risk_band"] = pd.cut(
        out["client_churn_risk_score"],
        bins=[-1, 35, 65, 100],
        labels=["Low risk", "Watch", "High risk"],
    )

    if SKLEARN_OK and len(out) >= 6:
        feat = out[
            [
                "impact_total",
                "expected_account_ltv_aed",
                "client_churn_risk_score",
                "response_probability",
                "urgency_score",
                "digital_maturity_score",
            ]
        ].copy()
        feat["response_probability"] = feat["response_probability"] * 100
        feat["impact_total"] = np.log1p(feat["impact_total"])
        feat["expected_account_ltv_aed"] = np.log1p(feat["expected_account_ltv_aed"])
        X = StandardScaler().fit_transform(feat)
        k = min(4, len(out))
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        out["segment_id"] = km.fit_predict(X)

        seg = (
            out.groupby("segment_id")[["impact_total", "client_churn_risk_score", "response_probability", "urgency_score"]]
            .mean()
            .reset_index()
        )
        seg["priority"] = (
            seg["impact_total"].rank(pct=True) * 0.45
            + seg["urgency_score"].rank(pct=True) * 0.25
            + seg["response_probability"].rank(pct=True) * 0.20
            + seg["client_churn_risk_score"].rank(pct=True) * 0.10
        )
        seg = seg.sort_values("priority", ascending=False).reset_index(drop=True)
        names = ["Scale now", "Prove & expand", "Protect value", "Nurture later"]
        mapping = {r["segment_id"]: names[i] for i, (_, r) in enumerate(seg.iterrows())}
        out["segment_name"] = out["segment_id"].map(mapping)
    else:
        score = (
            out["impact_total"].rank(pct=True) * 0.45
            + out["urgency_score"].rank(pct=True) * 0.25
            + out["response_probability"].rank(pct=True) * 0.20
            + out["client_churn_risk_score"].rank(pct=True) * 0.10
        )
        out["segment_name"] = pd.qcut(
            score.rank(method="first"),
            4,
            labels=["Nurture later", "Protect value", "Prove & expand", "Scale now"],
        )

    return out


def comparable_accounts(filtered, row):
    subset = filtered.copy()
    subset["distance"] = (
        (subset["revenue_aed_bn"] - row["revenue_aed_bn"]).abs() * 2
        + (subset["urgency_score"] - row["urgency_score"]).abs() * 0.45
        + (subset["expected_annual_contract_value_aed"] - row["expected_annual_contract_value_aed"]).abs() / 500000
    )
    subset = subset[subset["company_name"] != row["company_name"]].sort_values("distance").head(6)
    out = subset[
        [
            "company_name",
            "sector",
            "segment_name",
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
            "segment_name": "Segment",
            "expected_account_ltv_aed": "Predicted LTV",
            "client_churn_risk_score": "Churn risk",
            "win_probability": "Win probability",
        }
    )


# -----------------------------
# Charts
# -----------------------------
def portfolio_bar(filtered, selected, p):
    top = (
        filtered[["company_name", "impact_total", "segment_name"]]
        .sort_values("impact_total", ascending=False)
        .head(12)
        .copy()
    )
    top["selected"] = np.where(top["company_name"] == selected, "Selected", "Peer")
    bars = alt.Chart(top).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("impact_total:Q", title="Modeled impact (AED)"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color(
            "selected:N",
            scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent"], p["danger"]]),
            legend=None,
        ),
        tooltip=["company_name", "segment_name", alt.Tooltip("impact_total:Q", format=",.0f")],
    )
    text = alt.Chart(top).mark_text(dx=8, align="left", font="Inter", fontSize=11, color=p["text"]).encode(
        x="impact_total:Q",
        y=alt.Y("company_name:N", sort="-x"),
        text=alt.Text("impact_total:Q", format=",.0f"),
    )
    return (bars + text).properties(title="Top accounts by modeled impact", height=340)


def impact_waterfall(model, p):
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
    df["Color"] = [p["success"], p["accent2"], p["accent"], p["accent3"], p["warn"], p["danger"]]

    bars = alt.Chart(df).mark_bar(cornerRadius=8).encode(
        x=alt.X("Driver:N", title=""),
        y=alt.Y("Start:Q", title="AED"),
        y2="End:Q",
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Driver", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-8, font="Inter", fontSize=11, color=p["text"]).encode(
        x="Driver:N",
        y="End:Q",
        text=alt.Text("Value:Q", format=",.0f"),
    )
    return (bars + text).properties(title="Impact decomposition waterfall", height=320)


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
    bars = alt.Chart(df).mark_bar(
        cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=42, opacity=0.75, color=p["accent"]
    ).encode(
        x=alt.X("Quarter:N", title=""),
        y=alt.Y("Pipeline inquiries:Q", title="Pipeline inquiries"),
        tooltip=["Quarter", "Pipeline inquiries", alt.Tooltip("Revenue growth %:Q", format=".1f")],
    )
    line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color=p["success"]).encode(
        x="Quarter:N",
        y=alt.Y("Revenue growth %:Q", title="Revenue growth %"),
    )
    return alt.layer(bars, line).resolve_scale(y="independent").properties(
        title="Sales motion: inquiries and growth",
        height=300,
    )


def segment_bubble_chart(filtered):
    df = (
        filtered.groupby("segment_name", as_index=False)
        .agg(
            accounts=("company_name", "count"),
            impact=("impact_total", "mean"),
            ltv=("expected_account_ltv_aed", "mean"),
            risk=("client_churn_risk_score", "mean"),
        )
        .copy()
    )
    df["impact_m"] = df["impact"] / 1_000_000
    return alt.Chart(df).mark_circle(opacity=0.85, stroke="white", strokeWidth=1).encode(
        x=alt.X("risk:Q", title="Average churn risk"),
        y=alt.Y("ltv:Q", title="Average predicted LTV (AED)"),
        size=alt.Size("accounts:Q", scale=alt.Scale(range=[500, 3000]), title="Accounts"),
        color=alt.Color("segment_name:N", title="Segment"),
        tooltip=[
            "segment_name",
            "accounts",
            alt.Tooltip("impact:Q", format=",.0f", title="Avg impact"),
            alt.Tooltip("ltv:Q", format=",.0f", title="Avg LTV"),
            alt.Tooltip("risk:Q", format=".1f", title="Avg churn risk"),
        ],
    ).properties(title="Customer segmentation map", height=340)


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


def ltv_risk_chart(filtered, selected, p):
    df = filtered.copy()
    df["selected"] = np.where(df["company_name"] == selected, "Selected", "Peer")
    base = alt.Chart(df).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("client_churn_risk_score:Q", title="Churn risk"),
        y=alt.Y("expected_account_ltv_aed:Q", title="Predicted LTV (AED)"),
        size=alt.Size("impact_total:Q", scale=alt.Scale(range=[80, 1200]), title="Impact"),
        color=alt.Color(
            "selected:N",
            scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent2"], p["danger"]]),
            legend=None,
        ),
        tooltip=[
            "company_name",
            "segment_name",
            alt.Tooltip("expected_account_ltv_aed:Q", format=",.0f"),
            alt.Tooltip("client_churn_risk_score:Q", format=".1f"),
            alt.Tooltip("impact_total:Q", format=",.0f"),
        ],
    )
    label = alt.Chart(df[df["company_name"] == selected]).mark_text(
        dx=8, dy=-8, font="Inter", fontSize=11, color=p["text"]
    ).encode(x="client_churn_risk_score:Q", y="expected_account_ltv_aed:Q", text="company_name:N")
    return (base + label).properties(title="LTV versus risk", height=340)


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
        pct = float((filtered[col] <= row[col]).mean() * 100)
        bucket = "Top quartile" if pct >= 75 else "Above median" if pct >= 50 else "Below median"
        rows.append({"Metric": label, "Percentile": pct, "Bucket": bucket})
    df = pd.DataFrame(rows).sort_values("Percentile", ascending=True)

    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("Percentile:Q", title="Percentile within filtered portfolio", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Metric:N", sort=None, title=""),
        color=alt.Color(
            "Bucket:N",
            scale=alt.Scale(domain=["Below median", "Above median", "Top quartile"], range=[p["warn"], p["accent"], p["success"]]),
            title="",
        ),
        tooltip=["Metric", alt.Tooltip("Percentile:Q", format=".1f")],
    )
    rule = alt.Chart(pd.DataFrame({"x": [50]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(x="x:Q")
    text = alt.Chart(df).mark_text(dx=8, align="left", color=p["text"], font="Inter", fontSize=11).encode(
        x="Percentile:Q", y=alt.Y("Metric:N", sort=None), text=alt.Text("Percentile:Q", format=".0f")
    )
    return (rule + bars + text).properties(title="Relative strength profile", height=300)


def next_action_timeline(row, model, p):
    close_days = int(row["expected_close_days"])
    phase1 = max(12, min(20, close_days // 2 if close_days > 2 else 12))
    phase2 = close_days
    phase3 = close_days + 30
    phase4 = max(phase3 + 25, int(row["next_service_expansion_days"]))
    df = pd.DataFrame(
        [
            {"Stage": "Diagnose + quantify", "Start": 0, "End": phase1, "Owner": "Commercial"},
            {"Stage": "Win sponsor + sign", "Start": phase1, "End": phase2, "Owner": "Commercial"},
            {"Stage": f"Launch {row['primary_fractional_cxo']}", "Start": phase2, "End": phase3, "Owner": row["primary_fractional_cxo"]},
            {"Stage": "Deploy AI layer", "Start": phase2 + 10, "End": phase3 + 18, "Owner": "AI layer"},
            {"Stage": f"Expand to {row['secondary_fractional_cxo']}", "Start": phase3, "End": phase4, "Owner": row["secondary_fractional_cxo"]},
        ]
    )
    bars = alt.Chart(df).mark_bar(cornerRadius=8, height=22).encode(
        x=alt.X("Start:Q", title="Days from today"),
        x2="End:Q",
        y=alt.Y("Stage:N", sort=None, title=""),
        color=alt.Color("Owner:N", title=""),
        tooltip=["Stage", "Owner", "Start", "End"],
    )
    rules = alt.Chart(pd.DataFrame({"x": [close_days, phase4]})).mark_rule(
        strokeDash=[6, 6], color=p["grid"]
    ).encode(x="x:Q")
    return (rules + bars).properties(title="Next purchase / expansion style timeline", height=300)


def response_matrix(filtered):
    return alt.Chart(filtered).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("response_probability:Q", title="Response probability"),
        y=alt.Y("incremental_uplift_pct:Q", title="Incremental uplift %"),
        size=alt.Size("expected_annual_contract_value_aed:Q", scale=alt.Scale(range=[80, 1200]), title="ACV"),
        color=alt.Color("segment_name:N", title="Segment"),
        tooltip=[
            "company_name",
            "segment_name",
            alt.Tooltip("response_probability:Q", format=".2f"),
            alt.Tooltip("incremental_uplift_pct:Q", format=".1f"),
            alt.Tooltip("expected_annual_contract_value_aed:Q", format=",.0f"),
        ],
    ).properties(title="Market response opportunity map", height=340)


def forecast_curve(row, model, p):
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
    return alt.Chart(long).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("Month:O", title="Month"),
        y=alt.Y("Value:Q", title="Cumulative value realized (AED)"),
        color=alt.Color(
            "Path:N",
            scale=alt.Scale(domain=["Conservative", "Base case", "Aggressive"], range=[p["warn"], p["accent"], p["success"]]),
            title="",
        ),
        tooltip=["Month", "Path", alt.Tooltip("Value:Q", format=",.0f")],
    ).properties(title="Sales / value forecast", height=300)


def experiment_chart(filtered, sample_size, p):
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
    seg["incremental_value_a"] = sample_size * (seg["variant_a"] - seg["control_conv"]) / 100 * seg["acv"]
    seg["incremental_value_b"] = sample_size * (seg["variant_b"] - seg["control_conv"]) / 100 * seg["acv"]

    long = pd.DataFrame(
        {
            "segment_name": np.repeat(seg["segment_name"].values, 3),
            "Arm": ["Control", "Variant A", "Variant B"] * len(seg),
            "Conv": np.concatenate([seg["control_conv"], seg["variant_a"], seg["variant_b"]]),
        }
    )

    return alt.Chart(long).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("segment_name:N", title=""),
        y=alt.Y("Conv:Q", title="Expected conversion %"),
        color=alt.Color("Arm:N", title=""),
        xOffset="Arm:N",
        tooltip=["segment_name", "Arm", alt.Tooltip("Conv:Q", format=".2f")],
    ).properties(title="A/B style experiment planner", height=320), seg


def geo_map(df, lat_col, lon_col):
    df_map = df[[lat_col, lon_col, "company_name", "impact_total", "segment_name"]].dropna().copy()
    if df_map.empty:
        return None

    df_map["radius"] = np.clip((df_map["impact_total"] / df_map["impact_total"].max()) * 40000 + 6000, 6000, 45000)
    view_state = pdk.ViewState(
        latitude=float(df_map[lat_col].mean()),
        longitude=float(df_map[lon_col].mean()),
        zoom=4,
        pitch=35,
    )
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        get_position=f"[{lon_col}, {lat_col}]",
        get_radius="radius",
        get_fill_color=[37, 99, 235, 160],
        pickable=True,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
    )
    tooltip = {
        "html": "<b>{company_name}</b><br/>Segment: {segment_name}<br/>Impact: {impact_total}",
        "style": {"backgroundColor": "#0F172A", "color": "white"},
    }
    return pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)


# -----------------------------
# App shell
# -----------------------------
df = load_data()
init_state(df)

with st.sidebar:
    st.subheader("Dashboard control")
    light = st.toggle("Light mode", value=st.session_state.appearance_mode == "Light")
    st.session_state.appearance_mode = "Light" if light else "Dark"

    if st.button("Reset filters", use_container_width=True):
        reset_filters(df)
        st.rerun()

    st.markdown("---")
    st.multiselect("Sector", sorted(df["sector"].dropna().unique()), key="flt_sector")
    st.multiselect("Primary CXO", sorted(df["primary_fractional_cxo"].dropna().unique()), key="flt_role")
    st.multiselect("Urgency tier", sorted(df["urgency_tier"].dropna().unique()), key="flt_urgency")
    st.multiselect("Account tier", sorted(df["account_tier"].dropna().unique()), key="flt_tier")
    st.slider("Revenue (AED bn)", float(df["revenue_aed_bn"].min()), float(df["revenue_aed_bn"].max()), key="flt_revenue")
    st.slider("Minimum win probability", 0.0, 1.0, key="flt_min_win", step=0.01)

    st.markdown("---")
    nav = st.radio(
        "Methodology view",
        [
            "Executive",
            "Metrics",
            "Segmentation",
            "Value & Risk",
            "Forecast & Response",
            "Geography",
            "Experiment Lab",
        ],
    )

palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)
inject_css(palette)

filtered = filtered_df(df)
if filtered.empty:
    st.warning("No companies match the current filters.")
    st.stop()

filtered = add_engineered_fields(filtered)

companies = sorted(filtered["company_name"].tolist())
if st.session_state.selected_company not in companies:
    st.session_state.selected_company = companies[0]

top1, top2, top3 = st.columns([6.2, 1.2, 1.2], gap="medium")
idx = companies.index(st.session_state.selected_company)
with top1:
    st.session_state.selected_company = st.selectbox("Selected company", companies, index=idx)
with top2:
    st.metric("Accounts in scope", len(filtered))
with top3:
    st.metric("Portfolio impact", fmt_aed(filtered["impact_total"].sum()))

row = filtered.loc[filtered["company_name"] == st.session_state.selected_company].iloc[0]
model = build_model(row, filtered)

pills = "".join(
    [
        f"<div class='pill'>Sector · {row['sector']}</div>",
        f"<div class='pill'>Revenue band · {row['revenue_band']}</div>",
        f"<div class='pill'>Primary wedge · {row['primary_fractional_cxo']}</div>",
        f"<div class='pill'>Segment · {row['segment_name']}</div>",
        f"<div class='pill'>Risk · {row['risk_band']}</div>",
        f"<div class='pill'>Close horizon · {row['close_horizon']}</div>",
    ]
)

hero_copy = (
    f"{row['company_name']} now sits inside a methodology-led view rather than a generic case-study dashboard. "
    f"It shows {fmt_aed(model['total'])} in modeled impact, {fmt_aed(row['expected_account_ltv_aed'])} predicted LTV, "
    f"{row['client_churn_risk_score']:.0f}/100 churn risk, and {row['segment_name']} as its analytics segment."
)

st.markdown(
    f"""
    <div class="hero">
        <h1 class="hero-title">Yalla Growth Analytics Studio</h1>
        <p class="hero-copy">{hero_copy}</p>
        <div class="pill-row">{pills}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="medium")
with k1:
    metric_card("Modeled impact", fmt_aed(model["total"]), "Composite of savings, AI attach, conversion, speed, process, and retention.")
with k2:
    metric_card("Predicted LTV", fmt_aed(row["expected_account_ltv_aed"]), "Portfolio value proxy for the account.")
with k3:
    metric_card("Churn risk", f"{row['client_churn_risk_score']:.0f}/100", "Retention pressure that could erode value.")
with k4:
    metric_card("Conviction", f"{model['conviction']:.0f}/100", "Blend of proof, urgency, and readiness.")
with k5:
    metric_card("Win probability", f"{row['win_probability']*100:.1f}%", "Commercial likelihood of closing.")
with k6:
    metric_card("Impact / cost", f"{model['payback']:.1f}x", "Modeled return divided by solution cost.")

if nav == "Executive":
    section_header(
        "Overview",
        "One page that tells the whole story",
        "Start with portfolio context, then move into value, risk, forecast, and action. This page is the MBA-style executive summary layer.",
    )
    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(portfolio_bar(filtered, row["company_name"], palette), use_container_width=True)
    with b:
        st.altair_chart(ltv_risk_chart(filtered, row["company_name"], palette), use_container_width=True)
        st.altair_chart(percentile_chart(filtered, row, palette), use_container_width=True)

    c, d = st.columns([0.56, 0.44], gap="large")
    with c:
        st.altair_chart(impact_waterfall(model, palette), use_container_width=True)
    with d:
        st.altair_chart(forecast_curve(row, model, palette), use_container_width=True)

    i1, i2, i3 = st.columns(3, gap="large")
    with i1:
        insight_card("Metrics lens", f"The commercial base is {fmt_aed(row['expected_annual_contract_value_aed'])} ACV with {row['expected_roi_multiple']:.2f}x expected ROI.")
    with i2:
        insight_card("Segment lens", f"This account falls into {row['segment_name']} with {row['client_churn_risk_score']:.0f}/100 churn risk and {row['response_probability']*100:.1f}% response probability.")
    with i3:
        insight_card("Action lens", f"Best next move: {row['ideal_next_action']}. Target expansion into {row['secondary_fractional_cxo']} in about {int(row['next_service_expansion_days'])} days.")

elif nav == "Metrics":
    section_header(
        "Know your metrics",
        "Represent the business as drivers, not just KPIs",
        "This view uses a decomposition mindset: how the value is built, how motion behaves over time, and where the company ranks in the current portfolio.",
    )
    a, b = st.columns([0.56, 0.44], gap="large")
    with a:
        st.altair_chart(impact_waterfall(model, palette), use_container_width=True)
    with b:
        st.altair_chart(portfolio_bar(filtered, row["company_name"], palette), use_container_width=True)

    c, d = st.columns([0.50, 0.50], gap="large")
    with c:
        st.altair_chart(quarterly_motion_chart(row, palette), use_container_width=True)
    with d:
        st.altair_chart(percentile_chart(filtered, row, palette), use_container_width=True)

    i1, i2 = st.columns(2, gap="large")
    with i1:
        insight_card("Why it works", "This section makes the account feel measurable. It shows decomposition, momentum, and portfolio standing instead of repeating the same card design.")
    with i2:
        insight_card("What to say", f"The best summary line is that {row['company_name']} has {fmt_aed(model['total'])} in modeled impact and sits strongest where value, urgency, and conversion logic overlap.")

elif nav == "Segmentation":
    section_header(
        "Customer segmentation",
        "Give the portfolio an actual shape",
        "This page turns the account universe into actionable groups, which makes the dashboard feel more analytical and less like a one-company pitch sheet.",
    )
    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(segment_bubble_chart(filtered), use_container_width=True)
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

elif nav == "Value & Risk":
    section_header(
        "LTV, churn, next move",
        "Show both upside and exposure",
        "This page covers lifetime value, retention risk, and timing so the reader sees not only who is valuable, but who needs action now.",
    )
    a, b = st.columns([0.55, 0.45], gap="large")
    with a:
        st.altair_chart(ltv_risk_chart(filtered, row["company_name"], palette), use_container_width=True)
    with b:
        st.altair_chart(percentile_chart(filtered, row, palette), use_container_width=True)
        st.altair_chart(next_action_timeline(row, model, palette), use_container_width=True)

    i1, i2, i3 = st.columns(3, gap="large")
    with i1:
        insight_card("Value", f"Predicted LTV is {fmt_aed(row['expected_account_ltv_aed'])}, which is the strongest value anchor for this page.")
    with i2:
        insight_card("Risk", f"Churn risk is {row['client_churn_risk_score']:.0f}/100, so the dashboard can frame both upside and value-at-risk.")
    with i3:
        insight_card("Timing", f"Expected close horizon is {int(row['expected_close_days'])} days and service expansion is expected in {int(row['next_service_expansion_days'])} days.")

    st.subheader("Closest comparable accounts")
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

elif nav == "Forecast & Response":
    section_header(
        "Sales and market response",
        "Blend forecasting with intervention logic",
        "This page combines time-based outlook with response and uplift style visuals, so the dashboard covers both prediction and actionability.",
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(forecast_curve(row, model, palette), use_container_width=True)
        st.altair_chart(quarterly_motion_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(response_matrix(filtered), use_container_width=True)
        scenario = pd.DataFrame(
            [
                {"Scenario": "Conservative", "Value": model["conservative"]},
                {"Scenario": "Base case", "Value": model["base"]},
                {"Scenario": "Aggressive", "Value": model["aggressive"]},
                {"Scenario": "Solution cost", "Value": float(row["fractional_ai_solution_cost_aed"])},
            ]
        )
        st.altair_chart(
            alt.Chart(scenario).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=58).encode(
                x=alt.X("Scenario:N", title=""),
                y=alt.Y("Value:Q", title="AED"),
                color=alt.Color("Scenario:N", title=""),
                tooltip=["Scenario", alt.Tooltip("Value:Q", format=",.0f")],
            ).properties(title="Forecast scenarios versus cost", height=300),
            use_container_width=True,
        )

elif nav == "Geography":
    section_header(
        "Map representation",
        "Only plot geography when the data truly has geography",
        "If latitude and longitude columns exist, this page becomes a live account map. If not, it clearly tells you what needs to be added.",
    )
    lat_col, lon_col = choose_geo_columns(filtered)
    if lat_col and lon_col:
        deck = geo_map(filtered, lat_col, lon_col)
        if deck:
            st.pydeck_chart(deck, use_container_width=True)
            st.caption(f"Using geo columns: {lat_col} and {lon_col}")
        else:
            st.info("Geo columns exist, but there are no non-null coordinates in the filtered view.")
    else:
        st.info(
            "No geographic coordinate columns were found. Add one latitude column and one longitude column such as latitude/longitude or lat/lon to unlock the live map."
        )

    geo_summary = (
        filtered.groupby("sector", as_index=False)
        .agg(accounts=("company_name", "count"), impact=("impact_total", "sum"))
        .sort_values("impact", ascending=False)
    )
    geo_summary["impact"] = geo_summary["impact"].map(fmt_aed)
    st.dataframe(geo_summary, use_container_width=True, hide_index=True)

elif nav == "Experiment Lab":
    section_header(
        "A/B testing and uplift",
        "Turn the dashboard into a decision system",
        "This page gives you a classroom-ready experiment layer with test-control thinking, offer variants, and segment-aware targeting.",
    )
    sample_size = st.slider("Target sample size per segment", 50, 5000, 500, 50)
    chart, seg = experiment_chart(filtered, sample_size, palette)
    a, b = st.columns([0.60, 0.40], gap="large")
    with a:
        st.altair_chart(chart, use_container_width=True)
    with b:
        seg_out = seg[["segment_name", "control_conv", "variant_a", "variant_b", "incremental_value_a", "incremental_value_b"]].copy()
        seg_out["control_conv"] = seg_out["control_conv"].round(2).astype(str) + "%"
        seg_out["variant_a"] = seg_out["variant_a"].round(2).astype(str) + "%"
        seg_out["variant_b"] = seg_out["variant_b"].round(2).astype(str) + "%"
        seg_out["incremental_value_a"] = seg_out["incremental_value_a"].map(fmt_aed)
        seg_out["incremental_value_b"] = seg_out["incremental_value_b"].map(fmt_aed)
        st.dataframe(seg_out, use_container_width=True, hide_index=True)

    i1, i2 = st.columns(2, gap="large")
    with i1:
        insight_card("How to present it", "Call this an experiment planner. It gives control vs variant thinking without needing raw historical A/B rows in the base CSV.")
    with i2:
        insight_card("Best class story", "Say that segmentation identifies where to test, response logic estimates expected conversion, and the experiment layer shows how to validate incremental value before scaling.")
        
st.download_button(
    "Download filtered dataset",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="yalla_growth_analytics_filtered.csv",
    mime="text/csv",
    use_container_width=True,
)
