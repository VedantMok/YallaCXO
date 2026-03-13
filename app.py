
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(page_title="Dubai Fractional CXO Prioritization OS", page_icon="📊", layout="wide")


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
                        p["accent"], p["accent_2"], p["accent_3"],
                        p["success"], p["danger"], p["warn"]
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
        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
        .stApp {{
            background:
                radial-gradient(circle at 8% 14%, {p['bg_grad_1']}, transparent 27%),
                radial-gradient(circle at 92% 8%, {p['bg_grad_2']}, transparent 24%),
                linear-gradient(180deg, {p['bg']} 0%, {p['bg']} 100%);
            color: {p['text']};
        }}
        .block-container {{ padding-top: 1rem; padding-bottom: 2.2rem; max-width: 1480px; }}
        section[data-testid="stSidebar"] {{ display: none; }}
        .hero {{
            background: linear-gradient(135deg, {p['hero_start']} 0%, {p['hero_mid']} 55%, {p['hero_end']} 100%);
            border: 1px solid {p['border']}; border-radius: 30px; padding: 1.55rem 1.75rem;
            box-shadow: {p['shadow']}; margin-bottom: 1rem;
        }}
        .hero-wrap {{ display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; }}
        .hero h1 {{ font-family:'Space Grotesk',sans-serif; margin:0; color:{p['text']}; font-size:2.15rem; }}
        .hero p {{ margin:.45rem 0 0 0; color:{p['muted']}; line-height:1.62; max-width:980px; }}
        .chip {{ display:inline-flex; align-items:center; padding:.48rem .76rem; border-radius:999px; background:{p['chip']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem; }}
        .banner {{ background:linear-gradient(135deg, rgba(37,99,235,0.11), rgba(20,184,166,0.10)); border:1px solid {p['border']}; border-radius:24px; padding:1.15rem 1.2rem; box-shadow:{p['shadow']}; margin-bottom:1rem; }}
        .banner h2 {{ font-family:'Space Grotesk',sans-serif; font-size:1.55rem; margin:0; color:{p['text']}; }}
        .banner p {{ margin:.25rem 0 0 0; color:{p['muted']}; line-height:1.58; max-width:980px; }}
        .pill-row {{ display:flex; gap:.55rem; flex-wrap:wrap; margin-top:.8rem; }}
        .pill {{ display:inline-flex; padding:.48rem .78rem; border-radius:999px; background:{p['pill']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem; }}
        .metric {{ background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; padding:1rem .96rem; min-height:124px; box-shadow:{p['shadow']}; }}
        .metric .label {{ font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; color:{p['muted']}; margin-bottom:.32rem; }}
        .metric .value {{ font-family:'Space Grotesk',sans-serif; font-size:1.45rem; font-weight:700; color:{p['text']}; line-height:1.1; margin-bottom:.25rem; }}
        .metric .sub {{ font-size:.84rem; color:{p['muted']}; line-height:1.45; }}
        .section-kicker {{ font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:{p['accent_2']}; margin-bottom:.26rem; }}
        .section-title {{ font-family:'Space Grotesk',sans-serif; font-size:1.32rem; color:{p['text']}; margin:.06rem 0 .18rem 0; }}
        .section-copy {{ color:{p['muted']}; line-height:1.58; margin-bottom:.95rem; max-width:1040px; }}
        .insight {{ background:{p['panel']}; border:1px solid {p['border']}; border-left:4px solid {p['accent']}; border-radius:18px; padding:1rem 1.02rem; box-shadow:{p['shadow']}; height:100%; }}
        .insight h4 {{ margin:0 0 .42rem 0; color:{p['text']}; font-size:1rem; }}
        .insight p {{ margin:0; color:{p['muted']}; line-height:1.56; }}
        .callout {{ background:linear-gradient(135deg, rgba(37,99,235,0.10), rgba(20,184,166,0.10)); border:1px solid {p['border']}; border-left:4px solid {p['accent']}; border-radius:22px; padding:1rem 1.1rem; margin:.85rem 0 1rem 0; box-shadow:{p['shadow']}; color:{p['text']}; line-height:1.6; }}
        .stTabs [data-baseweb="tab-list"] {{ gap:.42rem; margin-bottom:.5rem; flex-wrap:wrap; }}
        .stTabs [data-baseweb="tab"] {{ background:{p['panel']}; border:1px solid {p['border']}; border-radius:14px; color:{p['muted']}; padding:.58rem .92rem; }}
        .stTabs [aria-selected="true"] {{ background:linear-gradient(180deg, rgba(37,99,235,0.12), rgba(20,184,166,0.12)); color:{p['text']}; border-color:{p['accent']}; }}
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{ background:{p['panel']}; border-color:{p['border']}; }}
        div[data-testid="stDataFrame"] {{ border:1px solid {p['border']}; border-radius:18px; overflow:hidden; }}
        @media (max-width: 920px) {{ .hero-wrap {{ flex-direction:column; }} }}
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


def band_from_pct(series, labels):
    return pd.cut(
        series.rank(pct=True),
        bins=[0.0, 0.25, 0.50, 0.75, 1.0],
        labels=labels,
        include_lowest=True,
    )


def safe_column(df, col, default=0.0):
    if col not in df.columns:
        return pd.Series([default] * len(df), index=df.index)
    return df[col]


def safe_value(row, col, default=0.0):
    return row[col] if col in row.index else default


ROLE_COLS = {
    "CFO": "cfo_need_score",
    "CTO": "cto_need_score",
    "CHRO": "chro_need_score",
    "CMO": "cmo_need_score",
    "COO": "coo_need_score",
}

ARCHETYPE_MAP = {
    "CFO": "Finance-stressed firms",
    "CTO": "Tech-transformation firms",
    "CHRO": "People-scaling firms",
    "CMO": "Marketing-efficiency firms",
    "COO": "Operational-efficiency firms",
}


def init_state(df):
    if "appearance_mode" not in st.session_state:
        st.session_state.appearance_mode = "Dark"
    if "selected_company" not in st.session_state:
        st.session_state.selected_company = sorted(df["company_name"].tolist())[0]
    defaults = {
        "flt_sector": sorted(df["sector"].dropna().unique()),
        "flt_role": sorted(df["primary_fractional_cxo"].dropna().unique()) if "primary_fractional_cxo" in df.columns else sorted(df["company_name"].dropna().unique()[:1]),
        "flt_urgency": sorted(df["urgency_tier"].dropna().unique()) if "urgency_tier" in df.columns else [],
        "flt_tier": sorted(df["account_tier"].dropna().unique()) if "account_tier" in df.columns else [],
        "flt_revenue": (float(df["revenue_aed_bn"].min()), float(df["revenue_aed_bn"].max())),
        "flt_min_win": 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_filters(df):
    st.session_state.flt_sector = sorted(df["sector"].dropna().unique())
    st.session_state.flt_role = sorted(df["primary_fractional_cxo"].dropna().unique()) if "primary_fractional_cxo" in df.columns else []
    st.session_state.flt_urgency = sorted(df["urgency_tier"].dropna().unique()) if "urgency_tier" in df.columns else []
    st.session_state.flt_tier = sorted(df["account_tier"].dropna().unique()) if "account_tier" in df.columns else []
    st.session_state.flt_revenue = (float(df["revenue_aed_bn"].min()), float(df["revenue_aed_bn"].max()))
    st.session_state.flt_min_win = 0.0


def filtered_df(df):
    mask = pd.Series(True, index=df.index)
    mask &= df["sector"].isin(st.session_state.flt_sector)
    if "primary_fractional_cxo" in df.columns and len(st.session_state.flt_role) > 0:
        mask &= df["primary_fractional_cxo"].isin(st.session_state.flt_role)
    if "urgency_tier" in df.columns and len(st.session_state.flt_urgency) > 0:
        mask &= df["urgency_tier"].isin(st.session_state.flt_urgency)
    if "account_tier" in df.columns and len(st.session_state.flt_tier) > 0:
        mask &= df["account_tier"].isin(st.session_state.flt_tier)
    mask &= df["revenue_aed_bn"].between(st.session_state.flt_revenue[0], st.session_state.flt_revenue[1])
    mask &= safe_column(df, "win_probability", 0.0) >= st.session_state.flt_min_win
    return df[mask].copy()


def derive_primary_secondary(row):
    scores = {role: float(safe_value(row, col, 0.0)) for role, col in ROLE_COLS.items()}
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ordered[0][0], ordered[1][0], ordered[0][1], ordered[1][1]


def add_engineered_fields(df):
    out = df.copy()

    primary_roles, secondary_roles, primary_scores, secondary_scores = [], [], [], []
    for _, row in out.iterrows():
        p_role, s_role, p_score, s_score = derive_primary_secondary(row)
        primary_roles.append(p_role)
        secondary_roles.append(s_role)
        primary_scores.append(p_score)
        secondary_scores.append(s_score)

    out["derived_primary_cxo"] = primary_roles
    out["derived_secondary_cxo"] = secondary_roles
    out["derived_primary_score"] = primary_scores
    out["derived_secondary_score"] = secondary_scores
    out["need_archetype"] = out["derived_primary_cxo"].map(ARCHETYPE_MAP)

    out["weighted_acv"] = safe_column(out, "expected_annual_contract_value_aed") * safe_column(out, "win_probability")
    out["weighted_ltv"] = safe_column(out, "expected_account_ltv_aed") * safe_column(out, "win_probability")
    out["savings_vs_ft_gap"] = safe_column(out, "full_time_equivalent_cost_aed") - safe_column(out, "fractional_ai_solution_cost_aed")
    roi = safe_column(out, "estimated_annual_savings_aed") / safe_column(out, "fractional_ai_solution_cost_aed").replace(0, np.nan)
    out["solution_roi_proxy"] = roi.replace([np.inf, -np.inf], np.nan).fillna(0)
    out["value_at_risk"] = safe_column(out, "expected_account_ltv_aed") * safe_column(out, "client_churn_risk_score") / 100.0
    out["response_pct"] = safe_column(out, "response_probability") * 100
    out["win_pct"] = safe_column(out, "win_probability") * 100

    out["priority_index"] = (
        0.30 * out["derived_primary_score"]
        + 0.20 * safe_column(out, "urgency_score")
        + 0.20 * out["win_pct"]
        + 0.15 * out["response_pct"]
        + 0.15 * safe_column(out, "account_health_score")
    )

    out["priority_band"] = band_from_pct(out["priority_index"], ["Watch", "Build", "Prioritize", "Act now"])
    out["ltv_band"] = band_from_pct(safe_column(out, "expected_account_ltv_aed"), ["Low", "Mid", "High", "Elite"])
    out["close_horizon"] = pd.cut(
        safe_column(out, "expected_close_days"),
        bins=[-1, 30, 60, 90, 9999],
        labels=["0-30d", "31-60d", "61-90d", "90d+"],
    )
    out["monthly_expected_close"] = np.clip(np.ceil(safe_column(out, "expected_close_days") / 30), 1, 6).astype(int)
    return out


def narrative(row):
    return (
        f"{row['company_name']} is being treated as a lead-prioritization and service-design case. "
        f"The strongest need is {row['derived_primary_cxo']} ({row['derived_primary_score']:.1f}), "
        f"the secondary recommendation is {row['derived_secondary_cxo']} ({row['derived_secondary_score']:.1f}), "
        f"and the account sits inside the {row['need_archetype'].lower()} group."
    )


def executive_hook(row):
    return (
        f"Expected ACV is {fmt_aed(row['expected_annual_contract_value_aed'])}, weighted ACV is {fmt_aed(row['weighted_acv'])}, "
        f"estimated annual savings are {fmt_aed(row['estimated_annual_savings_aed'])}, and the service is benchmarked against "
        f"{fmt_aed(row['full_time_equivalent_cost_aed'])} in full-time executive cost."
    )


def portfolio_leaderboard(filtered, row, p):
    top = filtered[["company_name", "priority_index", "weighted_acv"]].sort_values("priority_index", ascending=False).head(15).copy()
    top["selected"] = np.where(top["company_name"] == row["company_name"], "Selected", "Peer")
    return alt.Chart(top).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("priority_index:Q", title="Priority index"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color("selected:N", scale=alt.Scale(domain=["Peer", "Selected"], range=[p["accent"], p["danger"]]), legend=None),
        tooltip=["company_name", alt.Tooltip("priority_index:Q", format=".1f"), alt.Tooltip("weighted_acv:Q", format=",.0f")],
    ).properties(title="Top accounts by priority index", height=360)


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


def north_star_bar(filtered):
    df = filtered.groupby("sector", as_index=False).agg(weighted_acv=("weighted_acv", "sum")).sort_values("weighted_acv", ascending=False).head(10)
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=38).encode(
        x=alt.X("sector:N", title="", sort="-y"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV (AED)"),
        color=alt.Color("sector:N", title=""),
        tooltip=["sector", alt.Tooltip("weighted_acv:Q", format=",.0f")],
    ).properties(title="North Star by sector: weighted ACV", height=320)


def role_profile_chart(row, p):
    df = pd.DataFrame({"Role": list(ROLE_COLS.keys()), "Need": [float(safe_value(row, ROLE_COLS[r], 0.0)) for r in ROLE_COLS]}).sort_values("Need", ascending=True)
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


def sector_role_heatmap(filtered):
    df = filtered.groupby(["sector", "derived_primary_cxo"], as_index=False).size().rename(columns={"size": "accounts"})
    heat = alt.Chart(df).mark_rect(cornerRadius=6).encode(
        x=alt.X("derived_primary_cxo:N", title="Primary CXO"),
        y=alt.Y("sector:N", title="Sector"),
        color=alt.Color("accounts:Q", scale=alt.Scale(scheme="tealblues"), title="Accounts"),
        tooltip=["sector", "derived_primary_cxo", "accounts"],
    )
    text = alt.Chart(df).mark_text(fontSize=11).encode(
        x="derived_primary_cxo:N", y="sector:N", text="accounts:Q",
        color=alt.condition(alt.datum.accounts > 2, alt.value("white"), alt.value("#0F172A")),
    )
    return (heat + text).properties(title="Sector by primary-CXO demand", height=360)


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
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=42, opacity=0.78, color=p["accent"]).encode(
        x=alt.X("Quarter:N", title=""),
        y=alt.Y("Pipeline inquiries:Q", title="Pipeline inquiries"),
        tooltip=["Quarter", "Pipeline inquiries", alt.Tooltip("Revenue growth %:Q", format=".1f")],
    )
    line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color=p["success"]).encode(
        x="Quarter:N", y=alt.Y("Revenue growth %:Q", title="Revenue growth %")
    )
    return alt.layer(bars, line).resolve_scale(y="independent").properties(title="Quarterly commercial motion", height=300)


def selected_value_donut(row):
    df = pd.DataFrame({
        "Driver": ["Savings", "Weighted ACV", "Weighted LTV", "Value at risk"],
        "Value": [
            float(safe_value(row, "estimated_annual_savings_aed", 0)),
            float(safe_value(row, "weighted_acv", 0)),
            float(safe_value(row, "weighted_ltv", 0)),
            float(safe_value(row, "value_at_risk", 0)),
        ],
    })
    return alt.Chart(df).mark_arc(innerRadius=68).encode(
        theta=alt.Theta("Value:Q"),
        color=alt.Color("Driver:N", title=""),
        tooltip=["Driver", alt.Tooltip("Value:Q", format=",.0f")],
    ).properties(title="Selected-company value mix", height=300)


def segment_bubble(filtered):
    df = filtered.groupby("need_archetype", as_index=False).agg(
        accounts=("company_name", "count"),
        avg_urgency=("urgency_score", "mean"),
        avg_savings=("estimated_annual_savings_aed", "mean"),
        avg_acv=("expected_annual_contract_value_aed", "mean"),
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
    df = filtered.groupby("need_archetype", as_index=False).agg(
        priority=("priority_index", "mean"),
        weighted_acv=("weighted_acv", "mean"),
    ).sort_values("priority", ascending=True)
    dots = alt.Chart(df).mark_circle(size=220, color=p["accent"]).encode(
        x=alt.X("priority:Q", title="Average priority index"),
        y=alt.Y("need_archetype:N", sort=None, title=""),
        tooltip=["need_archetype", alt.Tooltip("priority:Q", format=".1f"), alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dx=10, align="left", color=p["text"], fontSize=11).encode(
        x="priority:Q", y=alt.Y("need_archetype:N", sort=None), text=alt.Text("weighted_acv:Q", format=",.0f")
    )
    return (dots + text).properties(title="Average priority by archetype", height=300)


def cost_savings_chart(row, p):
    df = pd.DataFrame([
        {"Metric": "Full-time CXO cost", "Value": float(safe_value(row, "full_time_equivalent_cost_aed", 0)), "Type": "Cost"},
        {"Metric": "Fractional + AI cost", "Value": float(safe_value(row, "fractional_ai_solution_cost_aed", 0)), "Type": "Cost"},
        {"Metric": "Estimated annual savings", "Value": float(safe_value(row, "estimated_annual_savings_aed", 0)), "Type": "Value"},
    ])
    df["Color"] = df["Type"].map({"Cost": p["danger"], "Value": p["success"]})
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=58).encode(
        x=alt.X("Metric:N", title=""),
        y=alt.Y("Value:Q", title="AED"),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Metric", alt.Tooltip("Value:Q", format=",.0f")],
    )
    text = alt.Chart(df).mark_text(dy=-10, color=p["text"], fontSize=11).encode(
        x="Metric:N", y="Value:Q", text=alt.Text("Value:Q", format=",.0f")
    )
    return (bars + text).properties(title="Cost benchmark versus savings", height=320)


def weighted_value_scatter(filtered, row, p):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    base = alt.Chart(df).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("weighted_acv:Q", title="Weighted ACV (AED)"),
        y=alt.Y("weighted_ltv:Q", title="Weighted LTV (AED)"),
        size=alt.Size("estimated_annual_savings_aed:Q", scale=alt.Scale(range=[80, 1300]), title="Savings"),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("priority_band:N", title="Priority band")),
        tooltip=["company_name", "priority_band", alt.Tooltip("weighted_acv:Q", format=",.0f"), alt.Tooltip("weighted_ltv:Q", format=",.0f")],
    )
    label = alt.Chart(df[df["selected"]]).mark_text(dx=8, dy=-8, fontSize=11, color=p["text"]).encode(
        x="weighted_acv:Q", y="weighted_ltv:Q", text="company_name:N"
    )
    return (base + label).properties(title="Weighted ACV versus weighted LTV", height=340)


def sector_savings_gap_chart(filtered):
    df = filtered.groupby("sector", as_index=False).agg(avg_gap=("savings_vs_ft_gap", "mean")).sort_values("avg_gap", ascending=False).head(12)
    return alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("avg_gap:Q", title="Average cost gap vs full-time hiring (AED)"),
        y=alt.Y("sector:N", sort="-x", title=""),
        color=alt.Color("sector:N", title=""),
        tooltip=["sector", alt.Tooltip("avg_gap:Q", format=",.0f")],
    ).properties(title="Average savings gap by sector", height=320)


def top_weighted_acv_chart(filtered):
    df = filtered[["company_name", "weighted_acv", "derived_primary_cxo"]].sort_values("weighted_acv", ascending=False).head(12)
    return alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("weighted_acv:Q", title="Weighted ACV (AED)"),
        y=alt.Y("company_name:N", sort="-x", title=""),
        color=alt.Color("derived_primary_cxo:N", title="Primary CXO"),
        tooltip=["company_name", "derived_primary_cxo", alt.Tooltip("weighted_acv:Q", format=",.0f")],
    ).properties(title="Top weighted-ACV accounts", height=320)


def close_horizon_chart(filtered):
    df = filtered.groupby("close_horizon", as_index=False).agg(accounts=("company_name", "count")).dropna()
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=60).encode(
        x=alt.X("close_horizon:N", title="Expected close horizon"),
        y=alt.Y("accounts:Q", title="Accounts"),
        color=alt.Color("close_horizon:N", title=""),
        tooltip=["close_horizon", "accounts"],
    ).properties(title="Expected close horizon mix", height=300)


def monthly_weighted_pipeline_chart(filtered, p):
    df = filtered.groupby("monthly_expected_close", as_index=False).agg(weighted_acv=("weighted_acv", "sum")).sort_values("monthly_expected_close")
    all_months = pd.DataFrame({"monthly_expected_close": [1, 2, 3, 4, 5, 6]})
    df = all_months.merge(df, on="monthly_expected_close", how="left").fillna(0)
    df["label"] = "M" + df["monthly_expected_close"].astype(int).astype(str)
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=48, color=p["accent"]).encode(
        x=alt.X("label:N", title="Expected close month"),
        y=alt.Y("weighted_acv:Q", title="Weighted ACV (AED)"),
        tooltip=["label", alt.Tooltip("weighted_acv:Q", format=",.0f")],
    )
    line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color=p["success"]).encode(x="label:N", y="weighted_acv:Q")
    return (bars + line).properties(title="Expected weighted pipeline by month", height=320)


def response_win_scatter(filtered, row, p):
    df = filtered.copy()
    df["selected"] = df["company_name"].eq(row["company_name"])
    base = alt.Chart(df).mark_circle(opacity=0.82, stroke="white", strokeWidth=0.7).encode(
        x=alt.X("response_pct:Q", title="Response probability %"),
        y=alt.Y("win_pct:Q", title="Win probability %"),
        size=alt.Size("expected_annual_contract_value_aed:Q", scale=alt.Scale(range=[80, 1200]), title="Expected ACV"),
        color=alt.condition(alt.datum.selected, alt.value(p["danger"]), alt.Color("derived_primary_cxo:N", title="Primary CXO")),
        tooltip=["company_name", "derived_primary_cxo", alt.Tooltip("response_pct:Q", format=".1f"), alt.Tooltip("win_pct:Q", format=".1f"), alt.Tooltip("expected_annual_contract_value_aed:Q", format=",.0f")],
    )
    label = alt.Chart(df[df["selected"]]).mark_text(dx=8, dy=-8, fontSize=11, color=p["text"]).encode(
        x="response_pct:Q", y="win_pct:Q", text="company_name:N"
    )
    return (base + label).properties(title="Response versus win probability", height=340)


def funnel_chart(row, p):
    touches = max(int(safe_value(row, "sales_touchpoints_90d", 0)), 1)
    responses = max(1, int(round(touches * float(safe_value(row, "response_probability", 0)) * 0.9)))
    meetings = max(int(safe_value(row, "meetings_booked_90d", 0)), 1 if responses > 1 else 0)
    proposals = max(int(safe_value(row, "proposal_count_90d", 0)), 1 if meetings > 1 else 0)
    closes = max(0.5, float(safe_value(row, "win_probability", 0)) * max(1, proposals))
    df = pd.DataFrame([
        {"Stage": "Touches", "Value": touches, "Color": p["accent_3"]},
        {"Stage": "Responses", "Value": responses, "Color": p["accent"]},
        {"Stage": "Meetings", "Value": meetings, "Color": p["accent_2"]},
        {"Stage": "Proposals", "Value": proposals, "Color": p["warn"]},
        {"Stage": "Expected closes", "Value": closes, "Color": p["success"]},
    ]).sort_values("Value", ascending=False)
    return alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X("Value:Q", title="Volume / expected outcome"),
        y=alt.Y("Stage:N", sort="-x", title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Stage", alt.Tooltip("Value:Q", format=".1f")],
    ).properties(title="Commercial conversion funnel", height=280)


def percentile_chart(filtered, row, p):
    metrics = [
        ("Savings", "estimated_annual_savings_aed"),
        ("Expected ACV", "expected_annual_contract_value_aed"),
        ("Weighted ACV", "weighted_acv"),
        ("Urgency", "urgency_score"),
        ("Win %", "win_pct"),
        ("Primary need", "derived_primary_score"),
    ]
    rows = []
    for label, col in metrics:
        pct = float((filtered[col] <= row[col]).mean() * 100)
        color = p["success"] if pct >= 75 else p["accent"] if pct >= 50 else p["warn"]
        rows.append({"Metric": label, "Percentile": pct, "Color": color})
    df = pd.DataFrame(rows).sort_values("Percentile", ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X("Percentile:Q", title="Percentile within filtered portfolio", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Metric:N", sort=None, title=""),
        color=alt.Color("Color:N", scale=None, legend=None),
        tooltip=["Metric", alt.Tooltip("Percentile:Q", format=".1f")],
    )
    rule = alt.Chart(pd.DataFrame({"x": [50]})).mark_rule(strokeDash=[6, 6], color=p["grid"]).encode(x="x:Q")
    text = alt.Chart(df).mark_text(dx=8, align="left", fontSize=11, color=p["text"]).encode(
        x="Percentile:Q", y=alt.Y("Metric:N", sort=None), text=alt.Text("Percentile:Q", format=".0f")
    )
    return (rule + bars + text).properties(title="Relative standing", height=300)


def process_people_chart(row, p):
    current = {
        "Decision speed": max(10, 100 - min(100, float(safe_value(row, "reporting_delay_days", 0)) * 3.0)),
        "People stability": max(5, 100 - float(safe_value(row, "attrition_rate_pct", 0)) * 2.2),
        "Execution quality": float(safe_value(row, "process_efficiency_score", 0)),
        "Commercial efficiency": min(100, float(safe_value(row, "lead_conversion_pct", 0)) * 8 + float(safe_value(row, "campaign_roi_x", 0)) * 12),
        "AI readiness": (float(safe_value(row, "digital_maturity_score", 0)) + float(safe_value(row, "data_maturity_score", 0))) / 2,
    }
    improved = {
        "Decision speed": min(100, current["Decision speed"] + 15),
        "People stability": min(100, current["People stability"] + 10),
        "Execution quality": min(100, current["Execution quality"] + 12),
        "Commercial efficiency": min(100, current["Commercial efficiency"] + 10),
        "AI readiness": min(100, current["AI readiness"] + 14),
    }
    rows = []
    for k in current:
        rows.append({"Dimension": k, "State": "Current state", "Score": current[k]})
        rows.append({"Dimension": k, "State": "Improved state", "Score": improved[k]})
    df = pd.DataFrame(rows)
    return alt.Chart(df).mark_bar(cornerRadius=6).encode(
        x=alt.X("Score:Q", title="Capability score", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Dimension:N", sort=None, title=""),
        xOffset="State:N",
        color=alt.Color("State:N", scale=alt.Scale(domain=["Current state", "Improved state"], range=[p["danger"], p["success"]]), title=""),
        tooltip=["Dimension", "State", alt.Tooltip("Score:Q", format=".1f")],
    ).properties(title="Current versus improved operating state", height=320)


def comparable_accounts(filtered, row):
    subset = filtered.copy()
    subset["distance"] = (
        (subset["revenue_aed_bn"] - row["revenue_aed_bn"]).abs() * 2
        + (subset["urgency_score"] - row["urgency_score"]).abs() * 0.45
        + (subset["expected_annual_contract_value_aed"] - row["expected_annual_contract_value_aed"]).abs() / 500000
    )
    subset = subset[subset["company_name"] != row["company_name"]].sort_values("distance").head(8)
    out = subset[[
        "company_name", "sector", "derived_primary_cxo", "need_archetype",
        "estimated_annual_savings_aed", "expected_annual_contract_value_aed", "win_pct"
    ]].copy()
    out["estimated_annual_savings_aed"] = out["estimated_annual_savings_aed"].map(fmt_aed)
    out["expected_annual_contract_value_aed"] = out["expected_annual_contract_value_aed"].map(fmt_aed)
    out["win_pct"] = out["win_pct"].round(1).astype(str) + "%"
    return out.rename(columns={
        "company_name": "Comparable company",
        "derived_primary_cxo": "Primary CXO",
        "need_archetype": "Archetype",
        "estimated_annual_savings_aed": "Savings",
        "expected_annual_contract_value_aed": "Expected ACV",
        "win_pct": "Win probability",
    })


def clean_summary_table(df):
    rows = [
        ["Rows", len(df)],
        ["Columns", len(df.columns)],
        ["Missing cells", int(df.isna().sum().sum())],
        ["Duplicate rows", int(df.duplicated().sum())],
        ["Sectors", int(df['sector'].nunique())],
        ["Companies", int(df['company_name'].nunique())],
    ]
    return pd.DataFrame(rows, columns=["Check", "Value"])


def on_company_change():
    st.session_state.selected_company = st.session_state.company_sel


# --------------------------------------------------
# App
# --------------------------------------------------
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
                <h1>Dubai Fractional CXO Prioritization OS</h1>
                <p>
                    A descriptive decision-support dashboard for the top 100 Dubai corporates. It prioritizes which company needs which fractional CXO,
                    identifies the secondary recommendation, quantifies savings versus full-time hiring, and frames AI-enabled add-ons without drifting into an overbuilt predictive stack.
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
        if "primary_fractional_cxo" in df.columns:
            st.multiselect("Primary CXO", sorted(df["primary_fractional_cxo"].dropna().unique()), key="flt_role")
    with f3:
        if "urgency_tier" in df.columns:
            st.multiselect("Urgency tier", sorted(df["urgency_tier"].dropna().unique()), key="flt_urgency")
    with f4:
        if "account_tier" in df.columns:
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

sel, prev_col, next_col = st.columns([6.4, 0.8, 0.8], gap="medium")
idx = available.index(st.session_state.selected_company) if st.session_state.selected_company in available else 0
with sel:
    st.selectbox(
        "Selected company",
        available,
        index=idx,
        key="company_sel",
        label_visibility="collapsed",
        on_change=on_company_change,
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

pills = "".join([
    f"<div class='pill'>Sector · {row['sector']}</div>",
    f"<div class='pill'>Revenue band · {safe_value(row, 'revenue_band', 'n/a')}</div>",
    f"<div class='pill'>Primary role · {row['derived_primary_cxo']}</div>",
    f"<div class='pill'>Secondary role · {row['derived_secondary_cxo']}</div>",
    f"<div class='pill'>Archetype · {row['need_archetype']}</div>",
    f"<div class='pill'>Priority band · {row['priority_band']}</div>",
    f"<div class='pill'>Close horizon · {row['close_horizon']}</div>",
])

st.markdown(
    f"""
    <div class='banner'>
        <h2>{row['company_name']}</h2>
        <p>{narrative(row)}</p>
        <div class='pill-row'>{pills}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="medium")
with k1:
    metric_card("Primary CXO", row["derived_primary_cxo"], f"Need score {row['derived_primary_score']:.1f}")
with k2:
    metric_card("Secondary CXO", row["derived_secondary_cxo"], f"Need score {row['derived_secondary_score']:.1f}")
with k3:
    metric_card("Expected ACV", fmt_aed(row["expected_annual_contract_value_aed"]), "Headline annual contract value.")
with k4:
    metric_card("Weighted ACV", fmt_aed(row["weighted_acv"]), "Expected value adjusted by win probability.")
with k5:
    metric_card("Savings", fmt_aed(row["estimated_annual_savings_aed"]), "Savings versus current-state executive setup.")
with k6:
    metric_card("Priority index", f"{row['priority_index']:.1f}", "Composite of need, urgency, response, win, and health.")

st.markdown(
    f"<div class='callout'><strong>Executive hook:</strong> {executive_hook(row)}</div>",
    unsafe_allow_html=True,
)

t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    "Executive",
    "Metrics",
    "Segmentation",
    "Value",
    "Pipeline",
    "Drilldown",
    "Data",
])

with t1:
    section_header(
        "North Star",
        "Lead prioritization overview",
        "This view keeps the assignment grounded in descriptive analytics: which accounts matter, why they matter, and how the selected company compares with the rest of the filtered portfolio.",
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(portfolio_leaderboard(filtered, row, palette), use_container_width=True)
    with b:
        st.altair_chart(urgency_value_scatter(filtered, row, palette), use_container_width=True)
    c, d = st.columns(2, gap="large")
    with c:
        st.altair_chart(north_star_bar(filtered), use_container_width=True)
    with d:
        st.altair_chart(selected_value_donut(row), use_container_width=True)

with t2:
    section_header(
        "Descriptive metrics",
        "Core distributions and comparisons",
        "These charts focus on KPI design, spread, and portfolio context rather than predictive complexity.",
    )
    a, b = st.columns([0.5, 0.5], gap="large")
    with a:
        st.altair_chart(role_profile_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(acv_boxplot(filtered), use_container_width=True)
    c, d = st.columns([0.54, 0.46], gap="large")
    with c:
        st.altair_chart(savings_histogram(filtered, palette), use_container_width=True)
    with d:
        st.altair_chart(percentile_chart(filtered, row, palette), use_container_width=True)

with t3:
    section_header(
        "Customer segmentation",
        "Demand archetypes and sector grouping",
        "This layer translates generic customer segmentation into a B2B corporate need-profile lens for CFO, CTO, CHRO, CMO, and COO demand.",
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(segment_bubble(filtered), use_container_width=True)
    with b:
        st.altair_chart(archetype_priority_dot(filtered, palette), use_container_width=True)
    st.altair_chart(segment_stack(filtered), use_container_width=True)
    st.altair_chart(sector_role_heatmap(filtered), use_container_width=True)

with t4:
    section_header(
        "Value modeling",
        "Savings and account-value logic",
        "This section stays within the assignment scope by modeling expected value, cost comparison, and account worth without turning the project into a heavy predictive stack.",
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(cost_savings_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(weighted_value_scatter(filtered, row, palette), use_container_width=True)
    c, d = st.columns([0.48, 0.52], gap="large")
    with c:
        st.altair_chart(sector_savings_gap_chart(filtered), use_container_width=True)
    with d:
        st.altair_chart(top_weighted_acv_chart(filtered), use_container_width=True)

with t5:
    section_header(
        "Pipeline planning",
        "Optional sales-planning layer",
        "This is the furthest the app goes toward forecasting: expected close timing, weighted pipeline, commercial motion, and funnel shape.",
    )
    a, b = st.columns([0.5, 0.5], gap="large")
    with a:
        st.altair_chart(close_horizon_chart(filtered), use_container_width=True)
    with b:
        st.altair_chart(monthly_weighted_pipeline_chart(filtered, palette), use_container_width=True)
    c, d = st.columns([0.52, 0.48], gap="large")
    with c:
        st.altair_chart(response_win_scatter(filtered, row, palette), use_container_width=True)
    with d:
        st.altair_chart(funnel_chart(row, palette), use_container_width=True)
    st.altair_chart(quarterly_motion_chart(row, palette), use_container_width=True)

with t6:
    section_header(
        "Company drilldown",
        "Why this company deserves attention",
        "The selected-company view combines role logic, comparable accounts, and a before-versus-after operating picture.",
    )
    a, b = st.columns([0.52, 0.48], gap="large")
    with a:
        st.altair_chart(process_people_chart(row, palette), use_container_width=True)
    with b:
        insight_card("Priority interpretation", f"This account ranks in the {row['priority_band']} band, with strongest demand for {row['derived_primary_cxo']} and second-order demand for {row['derived_secondary_cxo']}.")
        insight_card("Value lens", f"Weighted ACV is {fmt_aed(row['weighted_acv'])}, weighted LTV is {fmt_aed(row['weighted_ltv'])}, and value at risk is {fmt_aed(row['value_at_risk'])}.")
        insight_card("Pricing lens", f"The service is priced against {fmt_aed(row['full_time_equivalent_cost_aed'])} in full-time cost and {fmt_aed(row['fractional_ai_solution_cost_aed'])} in fractional-plus-AI cost.")
    st.subheader("Closest comparable accounts")
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

with t7:
    section_header(
        "Data quality",
        "Synthetic-data validation and export",
        "This makes the individual assignment logic explicit: synthetic data, cleaning checks, transformation outputs, and downloadable evidence.",
    )
    a, b = st.columns([0.36, 0.64], gap="large")
    with a:
        st.dataframe(clean_summary_table(filtered), use_container_width=True, hide_index=True)
    with b:
        preview_cols = [
            "company_name", "sector", "revenue_aed_bn", "derived_primary_cxo", "derived_secondary_cxo",
            "priority_index", "weighted_acv", "estimated_annual_savings_aed", "close_horizon"
        ]
        st.dataframe(filtered[preview_cols].sort_values("priority_index", ascending=False), use_container_width=True, hide_index=True)

st.download_button(
    "Download filtered dataset",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="dubai_fractional_cxo_filtered.csv",
    mime="text/csv",
    use_container_width=True,
)
