import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO Impact Studio", page_icon="🚀", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def get_palette(mode: str):
    if mode == "Light":
        return {
            "bg": "#F5F7FB", "bg_grad_1": "rgba(59, 130, 246, 0.08)", "bg_grad_2": "rgba(20, 184, 166, 0.08)",
            "panel": "rgba(255,255,255,0.86)", "panel_solid": "#FFFFFF", "border": "rgba(15, 23, 42, 0.08)",
            "text": "#0F172A", "muted": "#5B6B7F", "accent": "#2563EB", "accent_2": "#14B8A6", "accent_3": "#7C3AED",
            "success": "#10B981", "danger": "#F97316", "warn": "#F59E0B", "pill_bg": "rgba(37,99,235,0.06)",
            "hero_start": "#EAF2FF", "hero_mid": "#F9FBFF", "hero_end": "#EEFFFB", "grid": "rgba(15,23,42,0.08)",
            "shadow": "0 16px 42px rgba(15,23,42,0.08)", "hero_chip": "rgba(37,99,235,0.09)"
        }
    return {
        "bg": "#0B1220", "bg_grad_1": "rgba(37, 99, 235, 0.12)", "bg_grad_2": "rgba(20, 184, 166, 0.10)",
        "panel": "rgba(15, 23, 42, 0.74)", "panel_solid": "#111827", "border": "rgba(148, 163, 184, 0.14)",
        "text": "#E8EEF8", "muted": "#A8B7CA", "accent": "#60A5FA", "accent_2": "#2DD4BF", "accent_3": "#A78BFA",
        "success": "#34D399", "danger": "#FB923C", "warn": "#FBBF24", "pill_bg": "rgba(96,165,250,0.08)",
        "hero_start": "#0F172A", "hero_mid": "#111827", "hero_end": "#10243B", "grid": "rgba(148,163,184,0.12)",
        "shadow": "0 18px 46px rgba(2,6,23,0.34)", "hero_chip": "rgba(96,165,250,0.10)"
    }


def enable_altair_theme(p):
    def theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": None},
                "title": {"color": p["text"], "fontSize": 18, "font": "Space Grotesk", "anchor": "start", "fontWeight": 700},
                "axis": {
                    "labelColor": p["muted"], "titleColor": p["text"], "gridColor": p["grid"], "domainColor": p["grid"],
                    "tickColor": p["grid"], "labelFont": "Inter", "titleFont": "Inter"
                },
                "legend": {"labelColor": p["muted"], "titleColor": p["text"], "labelFont": "Inter", "titleFont": "Inter"},
                "range": {"category": [p["accent"], p["accent_2"], p["accent_3"], p["success"], p["danger"], p["warn"]]}
            }
        }
    try:
        alt.themes.register("yalla_impact_theme", theme)
    except Exception:
        pass
    alt.themes.enable("yalla_impact_theme")


def inject_css(p):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] {{font-family: 'Inter', sans-serif;}}
    .stApp {{
        background: radial-gradient(circle at 10% 15%, {p['bg_grad_1']}, transparent 28%), radial-gradient(circle at 92% 8%, {p['bg_grad_2']}, transparent 24%), linear-gradient(180deg, {p['bg']} 0%, {p['bg']} 100%);
        color: {p['text']};
    }}
    .block-container {{padding-top: 1.0rem; padding-bottom: 2.2rem; max-width: 1460px;}}
    section[data-testid="stSidebar"] {{display:none;}}
    .hero {{background: linear-gradient(135deg, {p['hero_start']} 0%, {p['hero_mid']} 55%, {p['hero_end']} 100%); border:1px solid {p['border']}; border-radius:28px; padding:1.55rem 1.7rem; box-shadow:{p['shadow']}; margin-bottom:1rem;}}
    .hero-top {{display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;}}
    .hero h1 {{font-family:'Space Grotesk', sans-serif; margin:0; color:{p['text']}; font-size:2.3rem;}}
    .hero p {{margin:.45rem 0 0 0; color:{p['muted']}; max-width:980px; line-height:1.6;}}
    .chip {{display:inline-flex; align-items:center; padding:.46rem .74rem; border-radius:999px; background:{p['hero_chip']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem;}}
    .card {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:24px; padding:1.2rem; box-shadow:{p['shadow']}; backdrop-filter: blur(12px); margin-bottom:1rem;}}
    .company-banner {{background:linear-gradient(135deg, rgba(37,99,235,0.10), rgba(20,184,166,0.10)); border:1px solid {p['border']}; border-radius:24px; padding:1.2rem 1.25rem; box-shadow:{p['shadow']}; margin-bottom:1rem;}}
    .company-banner h2 {{font-family:'Space Grotesk', sans-serif; margin:0; color:{p['text']}; font-size:1.6rem;}}
    .company-banner p {{margin:.25rem 0 0 0; color:{p['muted']}; line-height:1.56; max-width:900px;}}
    .meta-row {{display:flex; gap:.55rem; flex-wrap:wrap; margin-top:.85rem;}}
    .meta-pill {{display:inline-flex; padding:.48rem .78rem; border-radius:999px; background:{p['pill_bg']}; color:{p['text']}; border:1px solid {p['border']}; font-size:.82rem;}}
    .kpi {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; padding:1rem .95rem; min-height:126px; box-shadow:{p['shadow']};}}
    .kpi .label {{font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; color:{p['muted']}; margin-bottom:.32rem;}}
    .kpi .value {{font-family:'Space Grotesk', sans-serif; font-size:1.52rem; color:{p['text']}; font-weight:700; line-height:1.1; margin-bottom:.25rem;}}
    .kpi .sub {{font-size:.84rem; color:{p['muted']}; line-height:1.45;}}
    .section-kicker {{font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:{p['accent_2']}; margin-bottom:.28rem;}}
    .section-title {{font-family:'Space Grotesk', sans-serif; color:{p['text']}; font-size:1.36rem; margin:.05rem 0 .18rem 0;}}
    .section-copy {{color:{p['muted']}; line-height:1.58; margin-bottom:.95rem; max-width:1000px;}}
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
    @media (max-width: 900px) {{ .hero-top {{flex-direction:column;}} }}
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


def pct(x):
    return f"{float(x):.1f}%"


def metric_card(label, value, sub):
    st.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div><div class='sub'>{sub}</div></div>", unsafe_allow_html=True)


def insight_card(title, text):
    st.markdown(f"<div class='insight'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def section_header(kicker, title, copy):
    st.markdown(f"<div class='section-kicker'>{kicker}</div><div class='section-title'>{title}</div><div class='section-copy'>{copy}</div>", unsafe_allow_html=True)


def z_pct(series, value):
    s = pd.Series(series).astype(float)
    std = float(s.std())
    if std == 0 or np.isnan(std):
        return 50.0
    z = (float(value) - float(s.mean())) / std
    score = 50 + 18 * z
    return float(max(0, min(100, score)))


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


def company_narrative(row):
    return (
        f"{row['company_name']} shows strongest demand for a {row['primary_fractional_cxo']}-led intervention, with {row['secondary_fractional_cxo']} as the next expansion lane. "
        f"The model suggests {fmt_aed(row['estimated_annual_savings_aed'])} in annual savings, {fmt_aed(row['expected_annual_contract_value_aed'])} in ACV, and {row['expected_roi_multiple']:.2f}x ROI if the solution is implemented."
    )


def build_impact_model(row, filtered):
    savings = float(row['estimated_annual_savings_aed'])
    ai_value = float(row['ai_attach_value_aed'])
    base_conv = float(row['baseline_conversion_probability'])
    uplift = float(row['incremental_uplift_pct']) / 100.0
    rec_acv = float(row['recommended_acv_aed'])
    uplift_value = max(0.0, rec_acv * base_conv * uplift)
    time_value = max(0.0, float(row['forecast_2q_revenue_aed']) * min(0.35, float(row['win_probability']) * 0.55))
    delivery_value = max(0.0, savings * (float(row['automation_potential_score']) / 100) * 0.18)
    people_value = max(0.0, savings * min(0.22, float(row['attrition_rate_pct']) / 100 * 0.55))
    total = savings + ai_value + uplift_value + time_value + delivery_value + people_value

    proof_strength = 0.35 * z_pct(filtered['estimated_annual_savings_aed'], row['estimated_annual_savings_aed']) + 0.35 * z_pct(filtered['expected_roi_multiple'], row['expected_roi_multiple']) + 0.30 * z_pct(filtered['win_probability'], row['win_probability'])
    urgency_pressure = 0.40 * float(row['urgency_score']) + 0.25 * float(row['cash_flow_volatility_score']) + 0.20 * float(row['project_backlog_score']) + 0.15 * float(row['compliance_risk_score'])
    scale_readiness = 0.35 * float(row['digital_maturity_score']) + 0.25 * float(row['data_maturity_score']) + 0.20 * float(row['account_health_score']) + 0.20 * float(row['cross_sell_readiness_score'])
    implementation_feasibility = 0.40 * (100 - float(row['expansion_complexity_score'])) + 0.25 * float(row['data_maturity_score']) + 0.20 * float(row['account_health_score']) + 0.15 * float(row['response_probability']) * 100
    conviction_score = 0.34 * proof_strength + 0.33 * urgency_pressure + 0.33 * scale_readiness

    return {
        'savings': savings,
        'ai_value': ai_value,
        'uplift_value': uplift_value,
        'time_value': time_value,
        'delivery_value': delivery_value,
        'people_value': people_value,
        'total_impact': total,
        'proof_strength': float(max(0, min(100, proof_strength))),
        'urgency_pressure': float(max(0, min(100, urgency_pressure))),
        'scale_readiness': float(max(0, min(100, scale_readiness))),
        'implementation_feasibility': float(max(0, min(100, implementation_feasibility))),
        'conviction_score': float(max(0, min(100, conviction_score))),
    }


def impact_bridge_chart(row, model, p):
    df = pd.DataFrame([
        {'Driver': 'Executive cost avoided', 'Value': model['savings'], 'Color': p['success']},
        {'Driver': 'AI attach value', 'Value': model['ai_value'], 'Color': p['accent_2']},
        {'Driver': 'Conversion uplift value', 'Value': model['uplift_value'], 'Color': p['accent']},
        {'Driver': 'Faster revenue capture', 'Value': model['time_value'], 'Color': p['accent_3']},
        {'Driver': 'Delivery efficiency upside', 'Value': model['delivery_value'], 'Color': p['warn']},
        {'Driver': 'People-risk reduction', 'Value': model['people_value'], 'Color': p['danger']},
    ]).sort_values('Value', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X('Value:Q', title='Modeled annual impact value (AED)'),
        y=alt.Y('Driver:N', sort=None, title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Driver', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(df).mark_text(dx=8, align='left', font='Inter', fontSize=11, color=p['text']).encode(
        x='Value:Q', y=alt.Y('Driver:N', sort=None), text=alt.Text('Value:Q', format=',.0f')
    )
    return (bars + text).properties(title='Impact stack: where the value comes from', height=320)


def executive_case_chart(row, filtered, model, p):
    data = [
        {'Dimension': 'Financial case', 'Score': 0.55 * z_pct(filtered['estimated_annual_savings_aed'], row['estimated_annual_savings_aed']) + 0.45 * z_pct(filtered['expected_roi_multiple'], row['expected_roi_multiple']), 'Color': p['success']},
        {'Dimension': 'Commercial readiness', 'Score': 0.60 * float(row['win_probability']) * 100 + 0.40 * float(row['response_probability']) * 100, 'Color': p['accent']},
        {'Dimension': 'Operational pain', 'Score': 0.35 * float(row['urgency_score']) + 0.35 * float(row['process_efficiency_score']) + 0.30 * float(row['project_backlog_score']), 'Color': p['danger']},
        {'Dimension': 'Scale potential', 'Score': 0.50 * float(row['upsell_propensity_score']) + 0.50 * float(row['cross_sell_readiness_score']), 'Color': p['accent_3']},
        {'Dimension': 'Implementation fit', 'Score': model['implementation_feasibility'], 'Color': p['accent_2']},
    ]
    df = pd.DataFrame(data).sort_values('Score', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X('Score:Q', title='Score out of 100', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Dimension:N', sort=None, title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Dimension', alt.Tooltip('Score:Q', format='.1f')]
    )
    rule = alt.Chart(pd.DataFrame({'x': [70]})).mark_rule(strokeDash=[6, 6], color=p['grid']).encode(x='x:Q')
    return (rule + bars).properties(title='Executive buying case: why this should be prioritized', height=300)


def problem_to_solution_chart(row, model, p):
    current = {
        'Decision speed': max(10, 100 - min(100, row['reporting_delay_days'] * 3.0)),
        'People stability': max(5, 100 - row['attrition_rate_pct'] * 2.2),
        'Execution efficiency': float(row['process_efficiency_score']),
        'Commercial efficiency': min(100, row['lead_conversion_pct'] * 8 + row['campaign_roi_x'] * 12),
        'Digital leverage': (float(row['digital_maturity_score']) + float(row['automation_potential_score'])) / 2,
    }
    improved = {
        'Decision speed': min(100, current['Decision speed'] + 18 + row['data_maturity_score'] * 0.08),
        'People stability': min(100, current['People stability'] + 10 + row['upsell_propensity_score'] * 0.05),
        'Execution efficiency': min(100, current['Execution efficiency'] + 12 + row['automation_potential_score'] * 0.08),
        'Commercial efficiency': min(100, current['Commercial efficiency'] + 10 + row['incremental_uplift_pct'] * 1.8 + row['response_probability'] * 12),
        'Digital leverage': min(100, current['Digital leverage'] + 10 + row['ai_attach_value_aed'] / max(1, row['expected_annual_contract_value_aed']) * 18),
    }
    rows = []
    for k in current:
        rows.append({'Dimension': k, 'State': 'Current state', 'Score': current[k]})
        rows.append({'Dimension': k, 'State': 'Post-implementation', 'Score': improved[k]})
    df = pd.DataFrame(rows)
    return alt.Chart(df).mark_bar(cornerRadius=6).encode(
        x=alt.X('Score:Q', title='Capability score', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Dimension:N', sort=None, title=''),
        color=alt.Color('State:N', scale=alt.Scale(domain=['Current state', 'Post-implementation'], range=[p['danger'], p['success']]), title=''),
        xOffset='State:N',
        tooltip=['Dimension', 'State', alt.Tooltip('Score:Q', format='.1f')]
    ).properties(title='Problem-to-outcome shift: what improves after deployment', height=320)


def urgency_vs_impact_chart(filtered, row, model, p):
    peers = filtered.copy()
    peers['impact_proxy'] = peers['estimated_annual_savings_aed'] + peers['ai_attach_value_aed'] + (peers['recommended_acv_aed'] * peers['baseline_conversion_probability'] * peers['incremental_uplift_pct'] / 100)
    peers['selected'] = peers['company_name'].eq(row['company_name'])
    base = alt.Chart(peers).mark_circle(opacity=0.78, stroke='white', strokeWidth=0.7).encode(
        x=alt.X('urgency_score:Q', title='Urgency score'),
        y=alt.Y('impact_proxy:Q', title='Impact proxy (AED)'),
        size=alt.Size('win_probability:Q', scale=alt.Scale(range=[70, 1000]), title='Win probability'),
        color=alt.condition(alt.datum.selected, alt.value(p['danger']), alt.Color('primary_fractional_cxo:N', title='Primary CXO')),
        tooltip=['company_name', 'sector', 'primary_fractional_cxo', alt.Tooltip('impact_proxy:Q', format=',.0f'), 'urgency_score', 'win_probability']
    )
    label = alt.Chart(peers[peers['selected']]).mark_text(dx=8, dy=-8, font='Inter', fontSize=11, color=p['text']).encode(
        x='urgency_score:Q', y='impact_proxy:Q', text='company_name:N'
    )
    return (base + label).properties(title='Priority map: impact potential versus urgency', height=340)


def proof_heatmap(row, model):
    df = pd.DataFrame([
        ('Pain', 'Urgency pressure', model['urgency_pressure']),
        ('Pain', 'Compliance risk', float(row['compliance_risk_score'])),
        ('Pain', 'Reporting friction', min(100, float(row['reporting_delay_days']) * 3.2)),
        ('Pain', 'Project backlog', float(row['project_backlog_score'])),
        ('Solution fit', 'Primary role fit', float(row['primary_need_score'])),
        ('Solution fit', 'AI leverage', float(row['automation_potential_score'])),
        ('Solution fit', 'Data readiness', float(row['data_maturity_score'])),
        ('Solution fit', 'Implementation feasibility', float(model['implementation_feasibility'])),
        ('Commercial', 'Win probability', float(row['win_probability']) * 100),
        ('Commercial', 'Response probability', float(row['response_probability']) * 100),
        ('Commercial', 'Upsell readiness', float(row['upsell_propensity_score'])),
        ('Commercial', 'Account health', float(row['account_health_score'])),
    ], columns=['Cluster', 'Metric', 'Score'])
    heat = alt.Chart(df).mark_rect(cornerRadius=6).encode(
        x=alt.X('Cluster:N', title=''),
        y=alt.Y('Metric:N', sort=None, title=''),
        color=alt.Color('Score:Q', scale=alt.Scale(scheme='tealblues'), title='Score'),
        tooltip=['Cluster', 'Metric', alt.Tooltip('Score:Q', format='.1f')]
    )
    text = alt.Chart(df).mark_text(font='Inter', fontSize=11).encode(
        x='Cluster:N', y=alt.Y('Metric:N', sort=None), text=alt.Text('Score:Q', format='.0f'),
        color=alt.condition(alt.datum.Score > 58, alt.value('white'), alt.value('#0F172A'))
    )
    return (heat + text).properties(title='Proof map: evidence the account is worth acting on', height=360)


def implementation_roadmap_chart(row, p):
    close_days = int(row['expected_close_days'])
    phase1_end = max(14, min(21, close_days // 2 if close_days > 2 else 14))
    phase2_end = close_days
    phase3_end = close_days + 30
    phase4_end = max(phase3_end + 20, int(row['next_service_expansion_days']))
    df = pd.DataFrame([
        {'Stage': 'Diagnose pain and quantify savings', 'Start': 0, 'End': phase1_end, 'Owner': 'Commercial'},
        {'Stage': 'Secure sponsor and close', 'Start': phase1_end, 'End': phase2_end, 'Owner': 'Commercial'},
        {'Stage': f'Deploy {row["primary_fractional_cxo"]}', 'Start': phase2_end, 'End': phase3_end, 'Owner': row['primary_fractional_cxo']},
        {'Stage': 'Activate AI agents and reporting layer', 'Start': phase2_end + 10, 'End': phase3_end + 20, 'Owner': 'AI layer'},
        {'Stage': f'Expand into {row["secondary_fractional_cxo"]}', 'Start': phase3_end, 'End': phase4_end, 'Owner': row['secondary_fractional_cxo']},
    ])
    bars = alt.Chart(df).mark_bar(cornerRadius=8, height=22).encode(
        x=alt.X('Start:Q', title='Days from today'), x2='End:Q', y=alt.Y('Stage:N', sort=None, title=''),
        color=alt.Color('Owner:N', title=''), tooltip=['Stage', 'Owner', 'Start', 'End']
    )
    rules = alt.Chart(pd.DataFrame({'x': [close_days, phase4_end]})).mark_rule(strokeDash=[6, 6], color=p['grid']).encode(x='x:Q')
    return (rules + bars).properties(title='Implementation path: land value fast, then expand', height=290)


def role_and_addon_chart(row, model, p):
    addon_count = max(1, len(str(row['ai_agent_addons']).split(';')))
    primary_val = model['savings'] * 0.55
    ai_val = model['ai_value'] + model['delivery_value']
    secondary_val = model['savings'] * 0.20 + model['uplift_value']
    rows = pd.DataFrame([
        {'Layer': f'{row["primary_fractional_cxo"]} lead', 'Value': primary_val, 'Color': p['accent']},
        {'Layer': f'AI layer ({addon_count} addons)', 'Value': ai_val, 'Color': p['accent_2']},
        {'Layer': f'{row["secondary_fractional_cxo"]} expansion', 'Value': secondary_val, 'Color': p['accent_3']},
    ])
    bars = alt.Chart(rows).mark_bar(cornerRadiusEnd=10, height=28).encode(
        x=alt.X('Value:Q', title='Modeled contribution to impact (AED)'),
        y=alt.Y('Layer:N', sort=None, title=''),
        color=alt.Color('Color:N', scale=None, legend=None),
        tooltip=['Layer', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(rows).mark_text(dx=8, align='left', color=p['text'], font='Inter', fontSize=11).encode(
        x='Value:Q', y=alt.Y('Layer:N', sort=None), text=alt.Text('Value:Q', format=',.0f')
    )
    return (bars + text).properties(title='Solution design: where the implementation value is created', height=220)


def comparable_accounts(filtered, row):
    subset = filtered.copy()
    subset['distance'] = (
        (subset['revenue_aed_bn'] - row['revenue_aed_bn']).abs() * 2
        + (subset['urgency_score'] - row['urgency_score']).abs() * 0.45
        + (subset['expected_annual_contract_value_aed'] - row['expected_annual_contract_value_aed']).abs() / 500000
    )
    subset = subset[subset['company_name'] != row['company_name']].sort_values('distance').head(5)
    out = subset[['company_name', 'sector', 'primary_fractional_cxo', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability']].copy()
    out['estimated_annual_savings_aed'] = out['estimated_annual_savings_aed'].map(fmt_aed)
    out['expected_annual_contract_value_aed'] = out['expected_annual_contract_value_aed'].map(fmt_aed)
    out['win_probability'] = (out['win_probability'] * 100).round(1).astype(str) + '%'
    return out.rename(columns={
        'company_name': 'Comparable company', 'sector': 'Sector', 'primary_fractional_cxo': 'Primary CXO',
        'estimated_annual_savings_aed': 'Savings', 'expected_annual_contract_value_aed': 'Expected ACV', 'win_probability': 'Win Prob.'
    })


def recommendation_text(row, model):
    return {
        'hook': f"Lead with the fact that {row['company_name']} has {fmt_aed(model['total_impact'])} in modeled annual impact on the table, not just a staffing problem.",
        'primary': f"Start with a {row['primary_fractional_cxo']}-led engagement because the account's strongest need score is {row['primary_need_score']:.1f}, and it links directly to the dominant pain pattern: {row['pain_archetype'].lower()}.",
        'expansion': f"After early proof, expand into {row['secondary_fractional_cxo']} and the AI layer to capture additional value from {row['ai_agent_addons']}.",
        'urgency': f"The account combines {row['urgency_score']:.1f} urgency, {row['win_probability']*100:.1f}% win probability, and a {int(row['expected_close_days'])}-day close horizon, so it should be treated as a near-term implementation candidate.",
    }


df = load_data()
init_state(df)
palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)
inject_css(palette)

st.markdown(f"<div class='hero'><div class='hero-top'><div><h1>Yalla CXO Impact Studio</h1><p>Move beyond demo dashboards. This version is built to show what the startup is actually solving, what value is at stake for each account, why the solution should be bought now, and how the implementation should unfold.</p></div><div class='chip'>{st.session_state.appearance_mode} mode</div></div></div>", unsafe_allow_html=True)

with st.expander('Setup: company, filters, and appearance', expanded=False):
    st.markdown("<div class='setup-shell'><div class='setup-head'><div class='setup-title'>Pitch setup</div><div class='setup-copy'>Use this panel to select the company, filter the universe, or switch appearance. Keep it collapsed when you want the deck-like experience.</div></div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.35, 0.55, 0.55], gap='large')
    with c1:
        company_options = sorted(df['company_name'].tolist())
        setup_index = company_options.index(st.session_state.selected_company) if st.session_state.selected_company in company_options else 0
        setup_company = st.selectbox('Company to pitch', company_options, index=setup_index, key='setup_selected_company')
        if setup_company != st.session_state.selected_company:
            st.session_state.selected_company = setup_company
    with c2:
        light_toggle = st.toggle('Light mode', value=st.session_state.appearance_mode == 'Light')
        st.session_state.appearance_mode = 'Light' if light_toggle else 'Dark'
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

available_companies = sorted(filtered['company_name'].tolist())
if st.session_state.selected_company not in available_companies:
    st.session_state.selected_company = available_companies[0]

sel, prev_col, next_col = st.columns([6.4, 0.8, 0.8], gap='medium')
with sel:
    st.selectbox('Selected company', available_companies, key='selected_company', label_visibility='collapsed')
idx = available_companies.index(st.session_state.selected_company)
with prev_col:
    if st.button('◀', use_container_width=True, disabled=idx == 0):
        st.session_state.selected_company = available_companies[idx - 1]
        st.rerun()
with next_col:
    if st.button('▶', use_container_width=True, disabled=idx == len(available_companies) - 1):
        st.session_state.selected_company = available_companies[idx + 1]
        st.rerun()

row = filtered.loc[filtered['company_name'] == st.session_state.selected_company].iloc[0]
model = build_impact_model(row, filtered)
rec = recommendation_text(row, model)

meta = ''.join([
    f"<div class='meta-pill'>Sector · {row['sector']}</div>",
    f"<div class='meta-pill'>Revenue band · {row['revenue_band']}</div>",
    f"<div class='meta-pill'>Primary role · {row['primary_fractional_cxo']}</div>",
    f"<div class='meta-pill'>Pain archetype · {row['pain_archetype']}</div>",
    f"<div class='meta-pill'>Urgency · {row['urgency_tier']} ({row['urgency_score']:.1f})</div>",
])
st.markdown(f"<div class='company-banner'><h2>{row['company_name']}</h2><p>{company_narrative(row)}</p><div class='meta-row'>{meta}</div></div>", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5, gap='medium')
with k1:
    metric_card('Total impact at stake', fmt_aed(model['total_impact']), 'Modeled value pool combining savings, AI attach, revenue uplift, speed, and execution upside.')
with k2:
    metric_card('Annual savings', fmt_aed(row['estimated_annual_savings_aed']), 'Core economic benefit from replacing full-time executive cost with the hybrid model.')
with k3:
    metric_card('Expected ROI', f"{row['expected_roi_multiple']:.2f}x", 'Return multiple if the proposed solution is implemented.')
with k4:
    metric_card('Conviction score', f"{model['conviction_score']:.0f}/100", 'Composite of proof strength, urgency pressure, and scale readiness.')
with k5:
    metric_card('Expected close horizon', f"{int(row['expected_close_days'])} days", 'Modeled time to secure the account and begin delivery.')

st.markdown(f"<div class='callout'><strong>Pitch hook:</strong> {rec['hook']} {rec['primary']} {rec['urgency']}</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(['Impact case', 'What problem exists', 'How value is created', 'Implementation case'])

with tab1:
    section_header('Executive case', 'Make the buyer feel the cost of inaction', 'This section is designed to answer the question every decision-maker asks first: is the problem large enough and urgent enough to justify implementation now?')
    a, b = st.columns([0.55, 0.45], gap='large')
    with a:
        st.altair_chart(impact_bridge_chart(row, model, palette), use_container_width=True)
    with b:
        st.altair_chart(executive_case_chart(row, filtered, model, palette), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Why this should get budget', f"The annual value pool is modeled at {fmt_aed(model['total_impact'])}, anchored by {fmt_aed(model['savings'])} in executive-cost avoidance and reinforced by AI attach, revenue capture, and efficiency gains.")
    with i2:
        insight_card('Why now', rec['urgency'])
    with i3:
        insight_card('Commercial proof', f"This account carries {row['win_probability']*100:.1f}% win probability, {row['response_probability']*100:.1f}% response probability, and {fmt_aed(row['weighted_pipeline_value_aed'])} in weighted pipeline value.")

with tab2:
    section_header('Problem evidence', 'Translate the startup into concrete pain, not abstract innovation', 'These visuals make the startup easier to buy because they show the underlying breakdown in capability, speed, and operating quality that the solution is actually fixing.')
    a, b = st.columns([0.52, 0.48], gap='large')
    with a:
        st.altair_chart(proof_heatmap(row, model), use_container_width=True)
    with b:
        st.altair_chart(problem_to_solution_chart(row, model, palette), use_container_width=True)
    i1, i2 = st.columns(2, gap='large')
    with i1:
        insight_card('Root problem', f"The model points to {row['pain_archetype'].lower()} as the dominant issue, with {row['primary_fractional_cxo']} showing the highest need score at {row['primary_need_score']:.1f}. This means the startup is solving a leadership-capacity gap plus a systems-execution gap, not just selling advisory time.")
    with i2:
        insight_card('Why the solution fits', f"The account combines {row['digital_maturity_score']:.0f} digital maturity, {row['automation_potential_score']:.0f} automation potential, and {row['data_maturity_score']:.0f} data maturity, which is strong enough to make the AI-supported model credible and implementable.")

with tab3:
    section_header('Value engine', 'Show exactly how the solution makes money or saves it', 'This section breaks the offer into economic logic so the reader understands how the startup creates measurable business impact after purchase.')
    a, b = st.columns([0.48, 0.52], gap='large')
    with a:
        st.altair_chart(role_and_addon_chart(row, model, palette), use_container_width=True)
    with b:
        st.altair_chart(urgency_vs_impact_chart(filtered, row, model, palette), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Primary implementation layer', f"Lead with {row['primary_fractional_cxo']} because it unlocks the biggest part of the modeled savings and validates the buying thesis fast.")
    with i2:
        insight_card('AI monetization layer', f"The AI layer contributes {fmt_aed(model['ai_value'] + model['delivery_value'])} in modeled value through attach revenue, better reporting, and process efficiency gains.")
    with i3:
        insight_card('Expansion logic', rec['expansion'])

with tab4:
    section_header('Implementation', 'Make the recommendation feel real, actionable, and low-friction', 'A strong business case needs a believable delivery path. This section shows how the account can move from diagnosis to proof to expansion with clear commercial timing.')
    a, b = st.columns([0.56, 0.44], gap='large')
    with a:
        st.altair_chart(implementation_roadmap_chart(row, palette), use_container_width=True)
    with b:
        insight_card('Suggested first action', f"Start with: {row['ideal_next_action']}. Use the initial engagement to quantify savings, align the sponsor, and establish the proof base for expansion.")
        insight_card('Implementation fit', f"The implementation-feasibility score is {model['implementation_feasibility']:.0f}/100, supported by {100-row['expansion_complexity_score']:.0f} complexity headroom, {row['data_maturity_score']:.0f} data maturity, and {row['account_health_score']:.0f} account health.")
        insight_card('Contract upside', f"If converted, the account supports {fmt_aed(row['expected_account_ltv_aed'])} in expected LTV across {int(row['expected_contract_term_months'])} months, with expansion potentially starting in {int(row['next_service_expansion_days'])} days.")
    st.subheader('Closest comparable accounts')
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
