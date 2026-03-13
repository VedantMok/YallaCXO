import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO Impact OS", page_icon="🚀", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def get_palette(mode: str):
    if mode == "Light":
        return {
            "bg": "#F5F7FB", "bg_grad_1": "rgba(59,130,246,0.08)", "bg_grad_2": "rgba(20,184,166,0.08)",
            "panel": "rgba(255,255,255,0.88)", "panel_solid": "#FFFFFF", "border": "rgba(15,23,42,0.08)",
            "text": "#0F172A", "muted": "#5B6B7F", "accent": "#2563EB", "accent_2": "#14B8A6", "accent_3": "#7C3AED",
            "success": "#10B981", "danger": "#F97316", "warn": "#F59E0B", "grid": "rgba(15,23,42,0.08)",
            "pill": "rgba(37,99,235,0.06)", "hero_start": "#EAF2FF", "hero_mid": "#F8FBFF", "hero_end": "#EEFFFB",
            "shadow": "0 16px 42px rgba(15,23,42,0.08)", "chip": "rgba(37,99,235,0.08)"
        }
    return {
        "bg": "#0B1220", "bg_grad_1": "rgba(37,99,235,0.12)", "bg_grad_2": "rgba(20,184,166,0.10)",
        "panel": "rgba(15,23,42,0.74)", "panel_solid": "#111827", "border": "rgba(148,163,184,0.14)",
        "text": "#E8EEF8", "muted": "#A8B7CA", "accent": "#60A5FA", "accent_2": "#2DD4BF", "accent_3": "#A78BFA",
        "success": "#34D399", "danger": "#FB923C", "warn": "#FBBF24", "grid": "rgba(148,163,184,0.12)",
        "pill": "rgba(96,165,250,0.08)", "hero_start": "#0F172A", "hero_mid": "#111827", "hero_end": "#10243B",
        "shadow": "0 18px 46px rgba(2,6,23,0.34)", "chip": "rgba(96,165,250,0.10)"
    }


def enable_altair_theme(p):
    def theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": None},
                "title": {"color": p["text"], "fontSize": 18, "font": "Space Grotesk", "anchor": "start", "fontWeight": 700},
                "axis": {"labelColor": p["muted"], "titleColor": p["text"], "gridColor": p["grid"], "domainColor": p["grid"], "tickColor": p["grid"], "labelFont": "Inter", "titleFont": "Inter"},
                "legend": {"labelColor": p["muted"], "titleColor": p["text"], "labelFont": "Inter", "titleFont": "Inter"},
                "range": {"category": [p["accent"], p["accent_2"], p["accent_3"], p["success"], p["danger"], p["warn"]]}
            }
        }
    try:
        alt.themes.register("yalla_impact_os", theme)
    except Exception:
        pass
    alt.themes.enable("yalla_impact_os")


def inject_css(p):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] {{font-family: 'Inter', sans-serif;}}
    .stApp {{background: radial-gradient(circle at 8% 14%, {p['bg_grad_1']}, transparent 27%), radial-gradient(circle at 92% 8%, {p['bg_grad_2']}, transparent 24%), linear-gradient(180deg, {p['bg']} 0%, {p['bg']} 100%); color: {p['text']};}}
    .block-container {{padding-top:1rem; padding-bottom:2.2rem; max-width: 1480px;}}
    section[data-testid="stSidebar"] {{display:none;}}
    .hero {{background: linear-gradient(135deg, {p['hero_start']} 0%, {p['hero_mid']} 55%, {p['hero_end']} 100%); border:1px solid {p['border']}; border-radius:30px; padding:1.55rem 1.75rem; box-shadow:{p['shadow']}; margin-bottom:1rem;}}
    .hero-wrap {{display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;}}
    .hero h1 {{font-family:'Space Grotesk',sans-serif; margin:0; color:{p['text']}; font-size:2.35rem;}}
    .hero p {{margin:.45rem 0 0 0; color:{p['muted']}; line-height:1.62; max-width:980px;}}
    .chip {{display:inline-flex; align-items:center; padding:.48rem .76rem; border-radius:999px; background:{p['chip']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem;}}
    .panel {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:24px; padding:1.18rem; box-shadow:{p['shadow']}; backdrop-filter: blur(12px); margin-bottom:1rem;}}
    .banner {{background:linear-gradient(135deg, rgba(37,99,235,0.11), rgba(20,184,166,0.10)); border:1px solid {p['border']}; border-radius:24px; padding:1.2rem 1.25rem; box-shadow:{p['shadow']}; margin-bottom:1rem;}}
    .banner h2 {{font-family:'Space Grotesk',sans-serif; font-size:1.62rem; margin:0; color:{p['text']};}}
    .banner p {{margin:.25rem 0 0 0; color:{p['muted']}; line-height:1.58; max-width:980px;}}
    .pill-row {{display:flex; gap:.55rem; flex-wrap:wrap; margin-top:.86rem;}}
    .pill {{display:inline-flex; padding:.48rem .78rem; border-radius:999px; background:{p['pill']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem;}}
    .metric {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; padding:1rem .96rem; min-height:128px; box-shadow:{p['shadow']};}}
    .metric .label {{font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; color:{p['muted']}; margin-bottom:.32rem;}}
    .metric .value {{font-family:'Space Grotesk',sans-serif; font-size:1.52rem; font-weight:700; color:{p['text']}; line-height:1.1; margin-bottom:.25rem;}}
    .metric .sub {{font-size:.84rem; color:{p['muted']}; line-height:1.45;}}
    .section-kicker {{font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:{p['accent_2']}; margin-bottom:.26rem;}}
    .section-title {{font-family:'Space Grotesk',sans-serif; font-size:1.36rem; color:{p['text']}; margin:.06rem 0 .18rem 0;}}
    .section-copy {{color:{p['muted']}; line-height:1.58; margin-bottom:.95rem; max-width:1040px;}}
    .insight {{background:{p['panel']}; border:1px solid {p['border']}; border-left:4px solid {p['accent']}; border-radius:18px; padding:1rem 1.02rem; box-shadow:{p['shadow']}; height:100%;}}
    .insight h4 {{margin:0 0 .42rem 0; color:{p['text']}; font-size:1rem;}}
    .insight p {{margin:0; color:{p['muted']}; line-height:1.56;}}
    .callout {{background:linear-gradient(135deg, rgba(37,99,235,0.10), rgba(20,184,166,0.10)); border:1px solid {p['border']}; border-left:4px solid {p['accent']}; border-radius:22px; padding:1rem 1.1rem; margin:.85rem 0 1rem 0; box-shadow:{p['shadow']}; color:{p['text']}; line-height:1.6;}}
    .stTabs [data-baseweb="tab-list"] {{gap:.55rem; margin-bottom:.45rem;}}
    .stTabs [data-baseweb="tab"] {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:14px; color:{p['muted']}; padding:.6rem 1rem;}}
    .stTabs [aria-selected="true"] {{background:linear-gradient(180deg, rgba(37,99,235,0.12), rgba(20,184,166,0.12)); color:{p['text']}; border-color:{p['accent']};}}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{background:{p['panel']}; border-color:{p['border']};}}
    div[data-testid="stDataFrame"] {{border:1px solid {p['border']}; border-radius:18px; overflow:hidden;}}
    details {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; box-shadow:{p['shadow']};}}
    details summary {{padding:.95rem 1rem;}}
    @media (max-width: 920px) {{.hero-wrap {{flex-direction:column;}}}}
    </style>
    """, unsafe_allow_html=True)


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
    st.markdown(f"<div class='metric'><div class='label'>{label}</div><div class='value'>{value}</div><div class='sub'>{sub}</div></div>", unsafe_allow_html=True)


def insight_card(title, text):
    st.markdown(f"<div class='insight'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def section_header(kicker, title, copy):
    st.markdown(f"<div class='section-kicker'>{kicker}</div><div class='section-title'>{title}</div><div class='section-copy'>{copy}</div>", unsafe_allow_html=True)


def z_score_pct(series, value):
    s = pd.Series(series).astype(float)
    std = float(s.std())
    if std == 0 or np.isnan(std):
        return 50.0
    z = (float(value) - float(s.mean())) / std
    return float(max(0, min(100, 50 + 18 * z)))


def init_state(df):
    if 'appearance_mode' not in st.session_state:
        st.session_state.appearance_mode = 'Dark'
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = sorted(df['company_name'].tolist())[0]
    defaults = {
        'flt_sector': sorted(df['sector'].unique()),
        'flt_role': sorted(df['primary_fractional_cxo'].unique()),
        'flt_urgency': sorted(df['urgency_tier'].unique()),
        'flt_tier': sorted(df['account_tier'].unique()),
        'flt_revenue': (float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max())),
        'flt_min_win': 0.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_filters(df):
    st.session_state.flt_sector = sorted(df['sector'].unique())
    st.session_state.flt_role = sorted(df['primary_fractional_cxo'].unique())
    st.session_state.flt_urgency = sorted(df['urgency_tier'].unique())
    st.session_state.flt_tier = sorted(df['account_tier'].unique())
    st.session_state.flt_revenue = (float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max()))
    st.session_state.flt_min_win = 0.0


def filtered_df(df):
    return df[
        df['sector'].isin(st.session_state.flt_sector)
        & df['primary_fractional_cxo'].isin(st.session_state.flt_role)
        & df['urgency_tier'].isin(st.session_state.flt_urgency)
        & df['account_tier'].isin(st.session_state.flt_tier)
        & df['revenue_aed_bn'].between(st.session_state.flt_revenue[0], st.session_state.flt_revenue[1])
        & (df['win_probability'] >= st.session_state.flt_min_win)
    ].copy()


def role_score(row, role_name):
    mapping = {
        'CFO': float(row['cfo_need_score']),
        'CTO': float(row['cto_need_score']),
        'CHRO': float(row['chro_need_score']),
        'CMO': float(row['cmo_need_score']),
        'COO': float(row['coo_need_score']),
    }
    return float(mapping.get(role_name, 0))


def build_model(row, filtered):
    savings = float(row['estimated_annual_savings_aed'])
    ai_attach = float(row['ai_attach_value_aed'])
    conv_uplift = float(row['recommended_acv_aed']) * float(row['baseline_conversion_probability']) * (float(row['incremental_uplift_pct']) / 100.0)
    speed_capture = float(row['forecast_2q_revenue_aed']) * min(0.34, float(row['win_probability']) * 0.55)
    process_uplift = savings * (float(row['automation_potential_score']) / 100.0) * 0.18
    people_risk = float(row['expected_account_ltv_aed']) * (float(row['client_churn_risk_score']) / 100.0) * 0.08
    total = savings + ai_attach + conv_uplift + speed_capture + process_uplift + people_risk

    proof = 0.34 * z_score_pct(filtered['estimated_annual_savings_aed'], row['estimated_annual_savings_aed']) + 0.33 * z_score_pct(filtered['expected_roi_multiple'], row['expected_roi_multiple']) + 0.33 * z_score_pct(filtered['win_probability'], row['win_probability'])
    urgency = 0.35 * float(row['urgency_score']) + 0.2 * float(row['cash_flow_volatility_score']) + 0.15 * float(row['compliance_risk_score']) + 0.15 * float(row['project_backlog_score']) + 0.15 * max(0, 100 - float(row['on_time_delivery_pct']))
    readiness = 0.28 * float(row['digital_maturity_score']) + 0.22 * float(row['data_maturity_score']) + 0.2 * float(row['account_health_score']) + 0.15 * float(row['cross_sell_readiness_score']) + 0.15 * float(row['response_probability']) * 100
    feasibility = 0.34 * (100 - float(row['expansion_complexity_score'])) + 0.22 * float(row['data_maturity_score']) + 0.22 * float(row['account_health_score']) + 0.22 * float(row['response_probability']) * 100
    conviction = 0.34 * proof + 0.33 * urgency + 0.33 * readiness

    conservative = total * 0.78
    base = total
    aggressive = total * 1.24

    return {
        'savings': savings,
        'ai_attach': ai_attach,
        'conv_uplift': conv_uplift,
        'speed_capture': speed_capture,
        'process_uplift': process_uplift,
        'people_risk': people_risk,
        'total': total,
        'proof': float(max(0, min(100, proof))),
        'urgency': float(max(0, min(100, urgency))),
        'readiness': float(max(0, min(100, readiness))),
        'feasibility': float(max(0, min(100, feasibility))),
        'conviction': float(max(0, min(100, conviction))),
        'conservative': conservative,
        'base': base,
        'aggressive': aggressive,
    }


def narrative(row, model):
    return (
        f"{row['company_name']} should be presented as an impact case, not a staffing case. The data suggests a {row['primary_fractional_cxo']}-led intervention addresses {row['pain_archetype'].lower()}, with {fmt_aed(model['total'])} in modeled value at stake across savings, AI monetization, revenue acceleration, and operational improvement."
    )


def recommendations(row, model):
    return {
        'hook': f"This account has {fmt_aed(model['total'])} in modeled value at stake and a conviction score of {model['conviction']:.0f}/100.",
        'why_now': f"Urgency is {row['urgency_score']:.1f}, win probability is {row['win_probability']*100:.1f}%, and the expected close horizon is {int(row['expected_close_days'])} days.",
        'why_solution': f"The strongest need score is {row['primary_need_score']:.1f} for {row['primary_fractional_cxo']}, with AI-supported expansion through {row['ai_supported_roles']} and {row['secondary_fractional_cxo']} after proof.",
        'proof': f"This case combines {fmt_aed(row['estimated_annual_savings_aed'])} in annual savings, {row['expected_roi_multiple']:.2f}x expected ROI, and {fmt_aed(row['expected_account_ltv_aed'])} expected LTV."
    }


def impact_stack_chart(model, p):
    df = pd.DataFrame([
        {'Driver': 'Executive cost avoided', 'Value': model['savings'], 'Color': p['success']},
        {'Driver': 'AI attach monetization', 'Value': model['ai_attach'], 'Color': p['accent_2']},
        {'Driver': 'Incremental conversion value', 'Value': model['conv_uplift'], 'Color': p['accent']},
        {'Driver': 'Faster revenue capture', 'Value': model['speed_capture'], 'Color': p['accent_3']},
        {'Driver': 'Process improvement upside', 'Value': model['process_uplift'], 'Color': p['warn']},
        {'Driver': 'Risk avoided / retention value', 'Value': model['people_risk'], 'Color': p['danger']},
    ]).sort_values('Value', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X('Value:Q', title='Modeled annual impact (AED)'),
        y=alt.Y('Driver:N', sort=None, title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Driver', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(df).mark_text(dx=8, align='left', font='Inter', fontSize=11, color=p['text']).encode(
        x='Value:Q', y=alt.Y('Driver:N', sort=None), text=alt.Text('Value:Q', format=',.0f')
    )
    return (bars + text).properties(title='Impact engine: what creates the value pool', height=320)


def scenario_chart(model, p):
    df = pd.DataFrame([
        {'Scenario': 'Conservative', 'Value': model['conservative'], 'Color': p['warn']},
        {'Scenario': 'Base case', 'Value': model['base'], 'Color': p['accent']},
        {'Scenario': 'Aggressive', 'Value': model['aggressive'], 'Color': p['success']},
    ])
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=58).encode(
        x=alt.X('Scenario:N', title=''),
        y=alt.Y('Value:Q', title='Annual impact value (AED)'),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Scenario', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(df).mark_text(dy=-10, font='Inter', fontSize=11, color=p['text']).encode(x='Scenario:N', y='Value:Q', text=alt.Text('Value:Q', format=',.0f'))
    return (bars + text).properties(title='Scenario view: downside, base, and upside', height=300)


def value_realization_chart(row, model, p):
    months = list(range(1, 13))
    base_curve = np.array([0.06, 0.12, 0.19, 0.28, 0.38, 0.49, 0.60, 0.70, 0.79, 0.87, 0.94, 1.00])
    cons_curve = np.array([0.04, 0.09, 0.15, 0.22, 0.31, 0.40, 0.50, 0.61, 0.71, 0.81, 0.90, 1.00])
    aggr_curve = np.array([0.08, 0.16, 0.25, 0.35, 0.46, 0.58, 0.69, 0.79, 0.87, 0.93, 0.97, 1.00])
    df = pd.DataFrame({
        'Month': months,
        'Conservative': model['conservative'] * cons_curve,
        'Base case': model['base'] * base_curve,
        'Aggressive': model['aggressive'] * aggr_curve,
    })
    long = df.melt('Month', var_name='Path', value_name='Value')
    chart = alt.Chart(long).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('Month:O', title='Month'),
        y=alt.Y('Value:Q', title='Cumulative value realized (AED)'),
        color=alt.Color('Path:N', scale=alt.Scale(domain=['Conservative', 'Base case', 'Aggressive'], range=[p['warn'], p['accent'], p['success']]), title=''),
        tooltip=['Month', 'Path', alt.Tooltip('Value:Q', format=',.0f')]
    )
    return chart.properties(title='Value realization over 12 months', height=300)


def cost_vs_return_chart(row, model, p):
    df = pd.DataFrame([
        {'Metric': 'Full-time executive stack', 'Value': float(row['full_time_equivalent_cost_aed']), 'Type': 'Cost'},
        {'Metric': 'Fractional + AI solution', 'Value': float(row['fractional_ai_solution_cost_aed']), 'Type': 'Cost'},
        {'Metric': 'Modeled impact created', 'Value': model['total'], 'Type': 'Return'},
    ])
    df['Color'] = df['Type'].map({'Cost': p['danger'], 'Return': p['success']})
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=55).encode(
        x=alt.X('Metric:N', title=''),
        y=alt.Y('Value:Q', title='AED value'),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Metric', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(df).mark_text(dy=-10, color=p['text'], font='Inter', fontSize=11).encode(x='Metric:N', y='Value:Q', text=alt.Text('Value:Q', format=',.0f'))
    return (bars + text).properties(title='Economics: cost of status quo versus return from action', height=320)


def executive_score_chart(row, model, p):
    df = pd.DataFrame([
        {'Dimension': 'Proof strength', 'Score': model['proof'], 'Color': p['success']},
        {'Dimension': 'Urgency pressure', 'Score': model['urgency'], 'Color': p['danger']},
        {'Dimension': 'Readiness', 'Score': model['readiness'], 'Color': p['accent_2']},
        {'Dimension': 'Feasibility', 'Score': model['feasibility'], 'Color': p['accent']},
        {'Dimension': 'Conviction', 'Score': model['conviction'], 'Color': p['accent_3']},
    ]).sort_values('Score', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=25).encode(
        x=alt.X('Score:Q', title='Score out of 100', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Dimension:N', sort=None, title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Dimension', alt.Tooltip('Score:Q', format='.1f')]
    )
    rule = alt.Chart(pd.DataFrame({'x':[70]})).mark_rule(strokeDash=[6,6], color=p['grid']).encode(x='x:Q')
    return (rule + bars).properties(title='Executive buying case', height=300)


def role_priority_chart(row, p):
    df = pd.DataFrame([
        {'Role': 'CFO', 'Need': float(row['cfo_need_score']), 'Enablement': (float(row['data_maturity_score']) + float(row['cash_flow_volatility_score'])) / 2},
        {'Role': 'CTO', 'Need': float(row['cto_need_score']), 'Enablement': (float(row['digital_maturity_score']) + float(row['cyber_risk_score'])) / 2},
        {'Role': 'CHRO', 'Need': float(row['chro_need_score']), 'Enablement': (100 - float(row['attrition_rate_pct']) * 2 + float(row['hiring_velocity_score'])) / 2},
        {'Role': 'CMO', 'Need': float(row['cmo_need_score']), 'Enablement': (float(row['campaign_roi_x']) * 22 + float(row['lead_conversion_pct']) * 4)},
        {'Role': 'COO', 'Need': float(row['coo_need_score']), 'Enablement': (float(row['process_efficiency_score']) + float(row['project_backlog_score'])) / 2},
    ])
    df['Priority'] = df['Need'] * 0.7 + df['Enablement'] * 0.3
    scatter = alt.Chart(df).mark_circle(opacity=0.88, stroke='white', strokeWidth=1).encode(
        x=alt.X('Enablement:Q', title='Operating evidence / enablement', scale=alt.Scale(domain=[0,100])),
        y=alt.Y('Need:Q', title='Executive need score', scale=alt.Scale(domain=[0,100])),
        size=alt.Size('Priority:Q', scale=alt.Scale(range=[180, 1400]), title='Priority'),
        color=alt.Color('Role:N', title=''),
        tooltip=['Role', alt.Tooltip('Need:Q', format='.1f'), alt.Tooltip('Enablement:Q', format='.1f'), alt.Tooltip('Priority:Q', format='.1f')]
    )
    labels = alt.Chart(df).mark_text(dy=-16, font='Inter', fontSize=11, color=p['text']).encode(x='Enablement:Q', y='Need:Q', text='Role:N')
    return (scatter + labels).properties(title='Role priority matrix: where intervention should start', height=320)


def proof_heatmap(row):
    df = pd.DataFrame([
        ('Pain', 'Urgency', float(row['urgency_score'])),
        ('Pain', 'Compliance risk', float(row['compliance_risk_score'])),
        ('Pain', 'Backlog pressure', float(row['project_backlog_score'])),
        ('Pain', 'Reporting friction', min(100, float(row['reporting_delay_days']) * 3.2)),
        ('Capability', 'Digital maturity', float(row['digital_maturity_score'])),
        ('Capability', 'Data maturity', float(row['data_maturity_score'])),
        ('Capability', 'Automation potential', float(row['automation_potential_score'])),
        ('Capability', 'Process efficiency', float(row['process_efficiency_score'])),
        ('Commercial', 'Win probability', float(row['win_probability']) * 100),
        ('Commercial', 'Response probability', float(row['response_probability']) * 100),
        ('Commercial', 'Upsell propensity', float(row['upsell_propensity_score'])),
        ('Commercial', 'Account health', float(row['account_health_score'])),
    ], columns=['Cluster','Metric','Score'])
    heat = alt.Chart(df).mark_rect(cornerRadius=6).encode(
        x=alt.X('Cluster:N', title=''),
        y=alt.Y('Metric:N', sort=None, title=''),
        color=alt.Color('Score:Q', scale=alt.Scale(scheme='tealblues'), title='Score'),
        tooltip=['Cluster','Metric', alt.Tooltip('Score:Q', format='.1f')]
    )
    text = alt.Chart(df).mark_text(font='Inter', fontSize=11).encode(
        x='Cluster:N', y=alt.Y('Metric:N', sort=None), text=alt.Text('Score:Q', format='.0f'),
        color=alt.condition(alt.datum.Score > 58, alt.value('white'), alt.value('#0F172A'))
    )
    return (heat + text).properties(title='Proof map: why the problem is real and solvable', height=360)


def before_after_chart(row, p):
    current = {
        'Decision speed': max(10, 100 - min(100, float(row['reporting_delay_days']) * 3.0)),
        'People stability': max(5, 100 - float(row['attrition_rate_pct']) * 2.2),
        'Execution quality': float(row['process_efficiency_score']),
        'Commercial efficiency': min(100, float(row['lead_conversion_pct']) * 8 + float(row['campaign_roi_x']) * 12),
        'AI leverage': (float(row['digital_maturity_score']) + float(row['automation_potential_score'])) / 2,
    }
    improved = {
        'Decision speed': min(100, current['Decision speed'] + 16 + float(row['data_maturity_score']) * 0.09),
        'People stability': min(100, current['People stability'] + 10 + float(row['upsell_propensity_score']) * 0.05),
        'Execution quality': min(100, current['Execution quality'] + 14 + float(row['automation_potential_score']) * 0.08),
        'Commercial efficiency': min(100, current['Commercial efficiency'] + 10 + float(row['incremental_uplift_pct']) * 1.8 + float(row['response_probability']) * 12),
        'AI leverage': min(100, current['AI leverage'] + 12 + float(row['ai_attach_value_aed']) / max(1, float(row['expected_annual_contract_value_aed'])) * 18),
    }
    rows = []
    for k in current:
        rows.append({'Dimension': k, 'State': 'Current state', 'Score': current[k]})
        rows.append({'Dimension': k, 'State': 'Post-implementation', 'Score': improved[k]})
    df = pd.DataFrame(rows)
    return alt.Chart(df).mark_bar(cornerRadius=6).encode(
        x=alt.X('Score:Q', title='Capability score', scale=alt.Scale(domain=[0,100])),
        y=alt.Y('Dimension:N', sort=None, title=''),
        xOffset='State:N',
        color=alt.Color('State:N', scale=alt.Scale(domain=['Current state', 'Post-implementation'], range=[p['danger'], p['success']]), title=''),
        tooltip=['Dimension','State', alt.Tooltip('Score:Q', format='.1f')]
    ).properties(title='Before and after: what the solution changes', height=320)


def revenue_motion_chart(row, p):
    df = pd.DataFrame({
        'Quarter': ['Q1','Q2','Q3','Q4'],
        'Pipeline inquiries': [int(row['q1_pipeline_inquiries']), int(row['q2_pipeline_inquiries']), int(row['q3_pipeline_inquiries']), int(row['q4_pipeline_inquiries'])],
        'Revenue growth %': [float(row['rev_growth_q1_pct']), float(row['rev_growth_q2_pct']), float(row['rev_growth_q3_pct']), float(row['rev_growth_q4_pct'])]
    })
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=42, opacity=0.78, color=p['accent']).encode(
        x=alt.X('Quarter:N', title=''),
        y=alt.Y('Pipeline inquiries:Q', title='Pipeline inquiries'),
        tooltip=['Quarter', 'Pipeline inquiries', alt.Tooltip('Revenue growth %:Q', format='.1f')]
    )
    line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color=p['success']).encode(
        x='Quarter:N',
        y=alt.Y('Revenue growth %:Q', title='Revenue growth %')
    )
    return alt.layer(bars, line).resolve_scale(y='independent').properties(title='Commercial motion: inquiry volume and revenue growth', height=300)


def funnel_chart(row, p):
    touches = max(int(row['sales_touchpoints_90d']), 1)
    responses = max(1, int(round(touches * float(row['response_probability']) * 0.9)))
    meetings = max(int(row['meetings_booked_90d']), 1 if responses > 1 else 0)
    proposals = max(int(row['proposal_count_90d']), 1 if meetings > 1 else 0)
    closes = max(0.5, float(row['win_probability']) * max(1, proposals))
    df = pd.DataFrame([
        {'Stage': 'Touches', 'Value': touches, 'Color': p['accent_3']},
        {'Stage': 'Responses', 'Value': responses, 'Color': p['accent']},
        {'Stage': 'Meetings', 'Value': meetings, 'Color': p['accent_2']},
        {'Stage': 'Proposals', 'Value': proposals, 'Color': p['warn']},
        {'Stage': 'Expected closes', 'Value': closes, 'Color': p['success']},
    ]).sort_values('Value', ascending=False)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X('Value:Q', title='Volume / expected outcome'),
        y=alt.Y('Stage:N', sort='-x', title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Stage', alt.Tooltip('Value:Q', format='.1f')]
    )
    return bars.properties(title='Commercial conversion funnel', height=280)


def peer_map_chart(filtered, row, p):
    peers = filtered.copy()
    peers['impact_proxy'] = peers['estimated_annual_savings_aed'] + peers['ai_attach_value_aed'] + (peers['recommended_acv_aed'] * peers['baseline_conversion_probability'] * peers['incremental_uplift_pct'] / 100)
    peers['selected'] = peers['company_name'].eq(row['company_name'])
    base = alt.Chart(peers).mark_circle(opacity=0.8, stroke='white', strokeWidth=0.7).encode(
        x=alt.X('urgency_score:Q', title='Urgency score'),
        y=alt.Y('impact_proxy:Q', title='Impact proxy (AED)'),
        size=alt.Size('win_probability:Q', scale=alt.Scale(range=[70,1000]), title='Win probability'),
        color=alt.condition(alt.datum.selected, alt.value(p['danger']), alt.Color('primary_fractional_cxo:N', title='Primary CXO')),
        tooltip=['company_name','sector','primary_fractional_cxo', alt.Tooltip('impact_proxy:Q', format=',.0f'), 'urgency_score','win_probability']
    )
    label = alt.Chart(peers[peers['selected']]).mark_text(dx=8, dy=-8, font='Inter', fontSize=11, color=p['text']).encode(x='urgency_score:Q', y='impact_proxy:Q', text='company_name:N')
    return (base + label).properties(title='Portfolio position: urgency versus impact', height=340)


def percentile_chart(filtered, row, p):
    metrics = [
        ('Savings', 'estimated_annual_savings_aed'),
        ('ACV', 'expected_annual_contract_value_aed'),
        ('Win probability', 'win_probability'),
        ('ROI', 'expected_roi_multiple'),
        ('Urgency', 'urgency_score'),
        ('LTV', 'expected_account_ltv_aed')
    ]
    rows = []
    for label, col in metrics:
        percentile = float((filtered[col] <= row[col]).mean() * 100)
        color = p['success'] if percentile >= 75 else p['accent'] if percentile >= 50 else p['warn']
        rows.append({'Metric': label, 'Percentile': percentile, 'Color': color})
    df = pd.DataFrame(rows).sort_values('Percentile', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X('Percentile:Q', title='Percentile within filtered portfolio', scale=alt.Scale(domain=[0,100])),
        y=alt.Y('Metric:N', sort=None, title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Metric', alt.Tooltip('Percentile:Q', format='.1f')]
    )
    rule = alt.Chart(pd.DataFrame({'x':[50]})).mark_rule(strokeDash=[6,6], color=p['grid']).encode(x='x:Q')
    text = alt.Chart(df).mark_text(dx=8, align='left', color=p['text'], font='Inter', fontSize=11).encode(x='Percentile:Q', y=alt.Y('Metric:N', sort=None), text=alt.Text('Percentile:Q', format='.0f'))
    return (rule + bars + text).properties(title='Relative strength: where this account stands', height=300)


def roadmap_chart(row, p):
    close_days = int(row['expected_close_days'])
    phase1 = max(12, min(20, close_days // 2 if close_days > 2 else 12))
    phase2 = close_days
    phase3 = close_days + 30
    phase4 = max(phase3 + 25, int(row['next_service_expansion_days']))
    df = pd.DataFrame([
        {'Stage': 'Diagnose pain and quantify impact', 'Start': 0, 'End': phase1, 'Owner': 'Commercial'},
        {'Stage': 'Secure sponsor and sign', 'Start': phase1, 'End': phase2, 'Owner': 'Commercial'},
        {'Stage': f'Launch {row["primary_fractional_cxo"]} workstream', 'Start': phase2, 'End': phase3, 'Owner': row['primary_fractional_cxo']},
        {'Stage': 'Deploy AI reporting + agents', 'Start': phase2 + 10, 'End': phase3 + 18, 'Owner': 'AI layer'},
        {'Stage': f'Expand into {row["secondary_fractional_cxo"]}', 'Start': phase3, 'End': phase4, 'Owner': row['secondary_fractional_cxo']},
    ])
    bars = alt.Chart(df).mark_bar(cornerRadius=8, height=22).encode(
        x=alt.X('Start:Q', title='Days from today'), x2='End:Q', y=alt.Y('Stage:N', sort=None, title=''),
        color=alt.Color('Owner:N', title=''), tooltip=['Stage', 'Owner', 'Start', 'End']
    )
    rules = alt.Chart(pd.DataFrame({'x':[close_days, phase4]})).mark_rule(strokeDash=[6,6], color=p['grid']).encode(x='x:Q')
    return (rules + bars).properties(title='Implementation path: land, prove, expand', height=290)


def comparable_accounts(filtered, row):
    subset = filtered.copy()
    subset['distance'] = ((subset['revenue_aed_bn'] - row['revenue_aed_bn']).abs() * 2 + (subset['urgency_score'] - row['urgency_score']).abs() * 0.45 + (subset['expected_annual_contract_value_aed'] - row['expected_annual_contract_value_aed']).abs() / 500000)
    subset = subset[subset['company_name'] != row['company_name']].sort_values('distance').head(6)
    out = subset[['company_name', 'sector', 'primary_fractional_cxo', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability']].copy()
    out['estimated_annual_savings_aed'] = out['estimated_annual_savings_aed'].map(fmt_aed)
    out['expected_annual_contract_value_aed'] = out['expected_annual_contract_value_aed'].map(fmt_aed)
    out['win_probability'] = (out['win_probability'] * 100).round(1).astype(str) + '%'
    return out.rename(columns={'company_name':'Comparable company','sector':'Sector','primary_fractional_cxo':'Primary CXO','estimated_annual_savings_aed':'Savings','expected_annual_contract_value_aed':'Expected ACV','win_probability':'Win Prob.'})


df = load_data()
init_state(df)
palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)
inject_css(palette)

st.markdown(f"<div class='hero'><div class='hero-wrap'><div><h1>Yalla CXO Impact OS</h1><p>A full revamp built to sell the solution, not just display the data. This version frames each company as a quantified business case with more graphs, clearer proof, stronger impact logic, and a believable implementation path.</p></div><div class='chip'>{st.session_state.appearance_mode} mode</div></div></div>", unsafe_allow_html=True)

with st.expander('Setup: company, filters, and appearance', expanded=False):
    c1, c2, c3 = st.columns([1.35, 0.55, 0.55], gap='large')
    with c1:
        options = sorted(df['company_name'].tolist())
        current = options.index(st.session_state.selected_company) if st.session_state.selected_company in options else 0
        setup_company = st.selectbox('Company to pitch', options, index=current, key='setup_selected_company')
        if setup_company != st.session_state.selected_company:
            st.session_state.selected_company = setup_company
    with c2:
        light = st.toggle('Light mode', value=st.session_state.appearance_mode == 'Light')
        st.session_state.appearance_mode = 'Light' if light else 'Dark'
    with c3:
        if st.button('Reset all filters', use_container_width=True):
            reset_filters(df)
            st.rerun()
    f1, f2, f3, f4 = st.columns(4, gap='large')
    with f1:
        st.multiselect('Sector', sorted(df['sector'].unique()), key='flt_sector')
    with f2:
        st.multiselect('Primary CXO', sorted(df['primary_fractional_cxo'].unique()), key='flt_role')
    with f3:
        st.multiselect('Urgency tier', sorted(df['urgency_tier'].unique()), key='flt_urgency')
    with f4:
        st.multiselect('Account tier', sorted(df['account_tier'].unique()), key='flt_tier')
    f5, f6 = st.columns([1.2, 0.8], gap='large')
    with f5:
        st.slider('Revenue (AED bn)', float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max()), key='flt_revenue')
    with f6:
        st.slider('Minimum win probability', 0.0, 1.0, key='flt_min_win', step=0.01)

palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)
filtered = filtered_df(df)
if filtered.empty:
    st.warning('No companies match the current filters.')
    st.stop()

available = sorted(filtered['company_name'].tolist())
if st.session_state.selected_company not in available:
    st.session_state.selected_company = available[0]

sel, prev_col, next_col = st.columns([6.4, 0.8, 0.8], gap='medium')
with sel:
    st.selectbox('Selected company', available, key='selected_company', label_visibility='collapsed')
idx = available.index(st.session_state.selected_company)
with prev_col:
    if st.button('◀', use_container_width=True, disabled=idx == 0):
        st.session_state.selected_company = available[idx - 1]
        st.rerun()
with next_col:
    if st.button('▶', use_container_width=True, disabled=idx == len(available) - 1):
        st.session_state.selected_company = available[idx + 1]
        st.rerun()

row = filtered.loc[filtered['company_name'] == st.session_state.selected_company].iloc[0]
model = build_model(row, filtered)
rec = recommendations(row, model)

pills = ''.join([
    f"<div class='pill'>Sector · {row['sector']}</div>",
    f"<div class='pill'>Revenue band · {row['revenue_band']}</div>",
    f"<div class='pill'>Primary role · {row['primary_fractional_cxo']}</div>",
    f"<div class='pill'>Pain archetype · {row['pain_archetype']}</div>",
    f"<div class='pill'>Urgency · {row['urgency_tier']} ({row['urgency_score']:.1f})</div>",
    f"<div class='pill'>Service package · {row['recommended_service_package']}</div>",
])
st.markdown(f"<div class='banner'><h2>{row['company_name']}</h2><p>{narrative(row, model)}</p><div class='pill-row'>{pills}</div></div>", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6, gap='medium')
with k1:
    metric_card('Impact at stake', fmt_aed(model['total']), 'Modeled value pool if the solution is implemented well.')
with k2:
    metric_card('Annual savings', fmt_aed(row['estimated_annual_savings_aed']), 'Direct savings versus a full-time executive stack.')
with k3:
    metric_card('Expected ROI', f"{row['expected_roi_multiple']:.2f}x", 'Financial return implied by the modeled solution.')
with k4:
    metric_card('Conviction score', f"{model['conviction']:.0f}/100", 'Composite of proof, urgency, and readiness.')
with k5:
    metric_card('Win probability', f"{row['win_probability']*100:.1f}%", 'Likelihood the account converts into an engagement.')
with k6:
    metric_card('Implementation fit', f"{model['feasibility']:.0f}/100", 'How practical the rollout looks from this data profile.')

st.markdown(f"<div class='callout'><strong>Executive hook:</strong> {rec['hook']} {rec['why_now']} {rec['why_solution']} {rec['proof']}</div>", unsafe_allow_html=True)

t1, t2, t3, t4, t5 = st.tabs(['Impact case', 'Evidence', 'Solution design', 'Commercial motion', 'Implementation'])

with t1:
    section_header('Impact story', 'Show the economic upside before anything else', 'This tab is built to make a reader feel the cost of delay. It quantifies where the value comes from, how much is realistic, and how quickly it can be realized.')
    a, b = st.columns([0.54, 0.46], gap='large')
    with a:
        st.altair_chart(impact_stack_chart(model, palette), use_container_width=True)
    with b:
        st.altair_chart(scenario_chart(model, palette), use_container_width=True)
    c, d = st.columns(2, gap='large')
    with c:
        st.altair_chart(value_realization_chart(row, model, palette), use_container_width=True)
    with d:
        st.altair_chart(cost_vs_return_chart(row, model, palette), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Budget argument', f"The buyer is not comparing the solution to zero. They are comparing it to the cost of status quo, which includes {fmt_aed(row['full_time_equivalent_cost_aed'])} in full-time executive cost and slower value capture.")
    with i2:
        insight_card('Upside view', f"The base case is {fmt_aed(model['base'])}, with upside to {fmt_aed(model['aggressive'])} if adoption, expansion, and AI attach land well.")
    with i3:
        insight_card('Why this feels real', f"The model ties impact to observed fields in the account: savings, response behavior, pipeline movement, AI attach value, and operating bottlenecks.")

with t2:
    section_header('Problem proof', 'Represent the problem so clearly that the solution feels inevitable', 'This tab connects pain signals, role fit, capability gaps, and portfolio ranking. The goal is to show what is broken, where it is broken, and why this startup is the right response.')
    a, b = st.columns([0.5, 0.5], gap='large')
    with a:
        st.altair_chart(proof_heatmap(row), use_container_width=True)
    with b:
        st.altair_chart(before_after_chart(row, palette), use_container_width=True)
    c, d = st.columns([0.52, 0.48], gap='large')
    with c:
        st.altair_chart(role_priority_chart(row, palette), use_container_width=True)
    with d:
        st.altair_chart(percentile_chart(filtered, row, palette), use_container_width=True)
    i1, i2 = st.columns(2, gap='large')
    with i1:
        insight_card('Root cause framing', f"The strongest need sits with {row['primary_fractional_cxo']} at {row['primary_need_score']:.1f}, while the operating profile shows friction in reporting, compliance, delivery, or talent depending on the account pattern.")
    with i2:
        insight_card('Why representation matters', 'The heatmap shows breadth of pain, the before-after bars show the improvement path, the role matrix shows where to begin, and the percentile chart shows why this account deserves attention versus peers.')

with t3:
    section_header('Solution architecture', 'Break the offer into layers so the value creation logic is visible', 'Readers buy faster when they can see how the solution works. This tab turns the recommendation into a structured intervention with roles, AI layers, and expansion logic.')
    a, b = st.columns([0.5, 0.5], gap='large')
    with a:
        st.altair_chart(executive_score_chart(row, model, palette), use_container_width=True)
    with b:
        st.altair_chart(role_priority_chart(row, palette), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Primary wedge', f"Start with {row['primary_fractional_cxo']} because it has the highest modeled need and the strongest link to the current pain pattern.")
    with i2:
        insight_card('AI layer', f"Use AI-supported roles ({row['ai_supported_roles']}) and addons like {row['ai_agent_addons']} to make the solution more scalable and more defensible.")
    with i3:
        insight_card('Expansion path', f"After initial proof, expand into {row['secondary_fractional_cxo']} within about {int(row['next_service_expansion_days'])} days to capture more of the value pool.")

with t4:
    section_header('Commercial momentum', 'Show that this is not only a strong idea, but also a winnable deal', 'This tab makes the business case stronger by showing whether the account is moving, engaging, and attractive relative to the portfolio.')
    a, b = st.columns([0.48, 0.52], gap='large')
    with a:
        st.altair_chart(revenue_motion_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(funnel_chart(row, palette), use_container_width=True)
    st.altair_chart(peer_map_chart(filtered, row, palette), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Pipeline signal', f"The quarterly inquiry pattern and revenue growth show whether the account is accelerating, plateauing, or losing momentum commercially.")
    with i2:
        insight_card('Conversion readiness', f"The account has {int(row['sales_touchpoints_90d'])} touches in 90 days, {int(row['meetings_booked_90d'])} meetings, and {int(row['proposal_count_90d'])} proposals, which helps explain closability.")
    with i3:
        insight_card('Portfolio context', 'The peer map tells the reader whether this company is a balanced high-impact opportunity or an outlier that needs extra caution.')

with t5:
    section_header('Implementation case', 'Make the solution look executable, not theoretical', 'A persuasive dashboard should end with confidence, not curiosity. This tab shows how the deal lands, how value is proven, and what comparable accounts look like.')
    a, b = st.columns([0.58, 0.42], gap='large')
    with a:
        st.altair_chart(roadmap_chart(row, palette), use_container_width=True)
    with b:
        insight_card('First move', f"Begin with: {row['ideal_next_action']}. Use the initial phase to quantify the value pool, align the sponsor, and shorten the path to commitment.")
        insight_card('Contract logic', f"Expected ACV is {fmt_aed(row['expected_annual_contract_value_aed'])}, expected LTV is {fmt_aed(row['expected_account_ltv_aed'])}, and the expected contract term is {int(row['expected_contract_term_months'])} months.")
        insight_card('Implementation confidence', f"Feasibility scores well because complexity headroom is {100-float(row['expansion_complexity_score']):.0f}, data maturity is {float(row['data_maturity_score']):.0f}, and account health is {float(row['account_health_score']):.0f}.")
    st.subheader('Closest comparable accounts')
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
