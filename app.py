import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO", page_icon="🚀", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def get_palette(mode: str):
    if mode == "Light":
        return {
            "bg": "#F5F7FB", "bg_grad_1": "rgba(61, 131, 255, 0.08)", "bg_grad_2": "rgba(16, 185, 129, 0.08)",
            "panel": "rgba(255,255,255,0.82)", "panel_solid": "#FFFFFF", "border": "rgba(15, 23, 42, 0.08)",
            "text": "#102033", "muted": "#5E738A", "soft": "#E9EEF5", "accent": "#2563EB", "accent_2": "#14B8A6",
            "accent_3": "#7C3AED", "success": "#10B981", "danger": "#F97316", "pill_bg": "rgba(37, 99, 235, 0.06)",
            "callout_start": "rgba(37, 99, 235, 0.08)", "callout_end": "rgba(20, 184, 166, 0.08)", "chart_text": "#102033",
            "chart_label": "#4B6075", "chart_grid": "rgba(15, 23, 42, 0.08)", "hero_start": "#EAF2FF", "hero_mid": "#F7FBFF",
            "hero_end": "#EEFFFB", "shadow": "0 16px 40px rgba(15,23,42,0.08)", "metric_cost": "#64748B", "metric_save": "#10B981",
            "highlight": "#2563EB",
        }
    return {
        "bg": "#0B1220", "bg_grad_1": "rgba(37, 99, 235, 0.12)", "bg_grad_2": "rgba(20, 184, 166, 0.10)",
        "panel": "rgba(15, 23, 42, 0.72)", "panel_solid": "#111827", "border": "rgba(148, 163, 184, 0.14)",
        "text": "#E8EEF8", "muted": "#9FB0C5", "soft": "#1E293B", "accent": "#60A5FA", "accent_2": "#2DD4BF",
        "accent_3": "#A78BFA", "success": "#34D399", "danger": "#FB923C", "pill_bg": "rgba(96, 165, 250, 0.08)",
        "callout_start": "rgba(96, 165, 250, 0.10)", "callout_end": "rgba(45, 212, 191, 0.10)", "chart_text": "#E8EEF8",
        "chart_label": "#AFC0D6", "chart_grid": "rgba(148, 163, 184, 0.12)", "hero_start": "#0F172A", "hero_mid": "#111827",
        "hero_end": "#10243B", "shadow": "0 18px 46px rgba(2,6,23,0.34)", "metric_cost": "#94A3B8", "metric_save": "#34D399",
        "highlight": "#60A5FA",
    }


def enable_altair_theme(p):
    def theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": None},
                "title": {"color": p["chart_text"], "fontSize": 18, "font": "Space Grotesk", "anchor": "start", "fontWeight": 700},
                "axis": {"labelColor": p["chart_label"], "titleColor": p["chart_text"], "gridColor": p["chart_grid"], "domainColor": p["chart_grid"], "tickColor": p["chart_grid"], "labelFont": "Inter", "titleFont": "Inter"},
                "legend": {"labelColor": p["chart_label"], "titleColor": p["chart_text"], "labelFont": "Inter", "titleFont": "Inter"},
                "range": {"category": [p["accent"], p["accent_2"], p["accent_3"], p["success"], p["danger"], "#FBBF24"]},
            }
        }
    try:
        alt.themes.register("yalla_descriptive_theme", theme)
    except Exception:
        pass
    alt.themes.enable("yalla_descriptive_theme")


def inject_css(p):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] {{font-family: 'Inter', sans-serif;}}
    .stApp {{background: radial-gradient(circle at 10% 20%, {p['bg_grad_1']}, transparent 28%), radial-gradient(circle at 90% 10%, {p['bg_grad_2']}, transparent 25%), linear-gradient(180deg, {p['bg']} 0%, {p['bg']} 100%); color: {p['text']};}}
    .block-container {{padding-top: 1.1rem; padding-bottom: 2rem; max-width: 1440px;}}
    section[data-testid="stSidebar"] {{display:none;}}
    .hero-shell {{background: linear-gradient(135deg, {p['hero_start']} 0%, {p['hero_mid']} 55%, {p['hero_end']} 100%); border: 1px solid {p['border']}; border-radius: 28px; padding: 1.55rem 1.75rem 1.35rem 1.75rem; box-shadow: {p['shadow']}; margin-bottom: 1rem; position: relative; overflow: hidden;}}
    .hero-top {{display:flex; align-items:flex-start; justify-content:space-between; gap:1rem;}}
    .hero-title {{font-family: 'Space Grotesk', sans-serif; font-size: 2.25rem; font-weight: 700; margin: 0; color: {p['text']};}}
    .hero-sub {{margin-top: .42rem; color: {p['muted']}; max-width: 980px; line-height: 1.6; font-size: 1rem;}}
    .mode-pill {{display:inline-flex; padding:.45rem .75rem; border-radius:999px; background:{p['pill_bg']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem;}}
    .glass-card {{background: {p['panel']}; border: 1px solid {p['border']}; border-radius: 24px; padding: 1.35rem; box-shadow: {p['shadow']}; backdrop-filter: blur(12px); margin-bottom: 1rem;}}
    .setup-shell {{background: {p['panel']}; border: 1px solid {p['border']}; border-radius: 22px; box-shadow: {p['shadow']}; overflow:hidden; margin-bottom:1rem;}}
    .setup-head {{padding:1rem 1.2rem; border-bottom:1px solid {p['border']}; background:linear-gradient(180deg, {p['callout_start']}, transparent);}}
    .setup-title {{font-family:'Space Grotesk',sans-serif; font-size:1.05rem; color:{p['text']};}}
    .setup-copy {{color:{p['muted']}; font-size:.88rem; margin-top:.16rem;}}
    .company-shell {{background: linear-gradient(135deg, {p['callout_start']} 0%, {p['callout_end']} 100%); border:1px solid {p['border']}; border-radius:22px; padding:1.15rem 1.2rem; box-shadow:{p['shadow']}; margin-bottom:1rem;}}
    .company-head {{display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;}}
    .company-title {{font-family:'Space Grotesk',sans-serif; font-size:1.55rem; color:{p['text']}; margin:0;}}
    .company-sub {{color:{p['muted']}; margin-top:.2rem; line-height:1.55; max-width:780px;}}
    .badge-row {{display:flex; gap:.6rem; flex-wrap:wrap; margin:.95rem 0 1.05rem 0;}}
    .badge-pill {{display:inline-flex; align-items:center; gap:.4rem; padding:.5rem .82rem; background:{p['pill_bg']}; color:{p['text']}; border:1px solid {p['border']}; border-radius:999px; font-size:.83rem; line-height:1;}}
    .section-kicker {{font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: {p['accent_2']}; margin-bottom: .32rem;}}
    .section-title {{font-family: 'Space Grotesk', sans-serif; color: {p['text']}; font-size: 1.36rem; margin: .1rem 0 .18rem 0;}}
    .section-copy {{color:{p['muted']}; line-height:1.58; margin-bottom:.95rem;}}
    .kpi-card {{background: {p['panel']}; border: 1px solid {p['border']}; border-radius: 22px; padding: 1rem .95rem .92rem .95rem; min-height: 126px; box-shadow: {p['shadow']};}}
    .kpi-label {{font-size: .74rem; text-transform: uppercase; letter-spacing: .08em; color: {p['muted']}; margin-bottom: .34rem;}}
    .kpi-value {{font-family: 'Space Grotesk', sans-serif; font-size: 1.52rem; font-weight: 700; color: {p['text']}; margin-bottom: .26rem; line-height:1.1;}}
    .kpi-sub {{font-size: .84rem; color: {p['muted']}; line-height: 1.45;}}
    .mini-stat-grid {{display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:.85rem; margin-top:.3rem;}}
    .mini-stat {{background: {p['pill_bg']}; border: 1px solid {p['border']}; border-radius: 18px; padding: .95rem 1rem; min-height: 104px;}}
    .mini-stat .label {{color:{p['muted']}; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em;}}
    .mini-stat .value {{font-family:'Space Grotesk',sans-serif; color:{p['text']}; font-size:1.15rem; margin-top:.22rem;}}
    .mini-stat .sub {{color:{p['muted']}; font-size:.82rem; margin-top:.22rem; line-height:1.45;}}
    .callout-box {{background: linear-gradient(135deg, {p['callout_start']} 0%, {p['callout_end']} 100%); border:1px solid {p['border']}; border-left: 4px solid {p['highlight']}; border-radius:22px; padding:1rem 1.1rem; margin:.8rem 0 1.1rem 0; box-shadow: {p['shadow']}; line-height:1.6; color: {p['text']};}}
    .insight-box {{background: {p['panel']}; border:1px solid {p['border']}; border-left:4px solid {p['accent']}; border-radius:18px; padding:1rem 1.02rem; box-shadow:{p['shadow']}; height:100%;}}
    .insight-box h4 {{margin:0 0 .45rem 0; color:{p['text']}; font-size:1rem;}}
    .insight-box p {{margin:0; color:{p['muted']}; line-height:1.56;}}
    .stTabs [data-baseweb="tab-list"] {{gap: .55rem; margin-bottom: .4rem;}}
    .stTabs [data-baseweb="tab"] {{background: {p['panel']}; border:1px solid {p['border']}; border-radius:14px; color:{p['muted']}; padding:.6rem 1rem;}}
    .stTabs [aria-selected="true"] {{background: linear-gradient(180deg, {p['callout_start']}, {p['callout_end']}); color:{p['text']}; border-color: {p['highlight']};}}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{background: {p['panel']}; border-color: {p['border']};}}
    div[data-testid="stDataFrame"] {{border:1px solid {p['border']}; border-radius:18px; overflow:hidden;}}
    details {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; box-shadow:{p['shadow']};}}
    details summary {{padding:.95rem 1rem;}}
    @media (max-width: 1100px) {{.mini-stat-grid {{grid-template-columns:1fr 1fr;}} .hero-title {{font-size: 1.9rem;}} .hero-top {{flex-direction:column;}}}}
    @media (max-width: 760px) {{.mini-stat-grid {{grid-template-columns:1fr;}} .company-head {{flex-direction:column;}}}}
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


def section_header(kicker, title, copy):
    st.markdown(f"<div class='section-kicker'>{kicker}</div><div class='section-title'>{title}</div><div class='section-copy'>{copy}</div>", unsafe_allow_html=True)


def insight_card(title, text):
    st.markdown(f"<div class='insight-box'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def kpi_card(title, value, subtitle):
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>{title}</div><div class='kpi-value'>{value}</div><div class='kpi-sub'>{subtitle}</div></div>", unsafe_allow_html=True)


def callout(text):
    st.markdown(f"<div class='callout-box'>{text}</div>", unsafe_allow_html=True)


def role_score(row, role_name):
    mapping = {
        'CFO': row['cfo_need_score'],
        'CTO': row['cto_need_score'],
        'CHRO': row['chro_need_score'],
        'CMO': row['cmo_need_score'],
        'COO': row['coo_need_score'],
    }
    return float(mapping.get(role_name, 0))


def role_profile_chart(row, p):
    df = pd.DataFrame({
        'Role': ['CFO', 'CTO', 'CHRO', 'CMO', 'COO'],
        'Need Score': [row['cfo_need_score'], row['cto_need_score'], row['chro_need_score'], row['cmo_need_score'], row['coo_need_score']]
    }).sort_values('Need Score', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X('Need Score:Q', title='Need Score', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Role:N', sort=None, title=''),
        color=alt.Color('Role:N', title=''),
        tooltip=['Role', alt.Tooltip('Need Score:Q', format='.1f')]
    )
    text = alt.Chart(df).mark_text(align='left', dx=8, color=p['chart_text'], font='Inter', fontSize=12).encode(
        x='Need Score:Q', y=alt.Y('Role:N', sort=None), text=alt.Text('Need Score:Q', format='.1f')
    )
    return (bars + text).properties(title='Executive need profile', height=300)


def operating_signal_chart(row):
    signals = pd.DataFrame({
        'Signal': ['Cash volatility', 'Digital maturity', 'Process efficiency', 'Attrition intensity', 'Campaign ROI signal', 'Win probability'],
        'Value': [row['cash_flow_volatility_score'], row['digital_maturity_score'], row['process_efficiency_score'], row['attrition_rate_pct'] * 3, row['campaign_roi_x'] * 20, row['win_probability'] * 100],
        'Category': ['Finance', 'Technology', 'Operations', 'People', 'Growth', 'Commercial']
    }).sort_values('Value', ascending=True)
    return alt.Chart(signals).mark_bar(cornerRadiusEnd=10, height=22).encode(
        x=alt.X('Value:Q', title='Scaled score / intensity'),
        y=alt.Y('Signal:N', sort=None, title=''),
        color=alt.Color('Category:N', title=''),
        tooltip=['Signal', 'Category', alt.Tooltip('Value:Q', format='.1f')]
    ).properties(title='Operating signal snapshot', height=300)


def company_cost_chart(row, p):
    df = pd.DataFrame({
        'Model': ['Full-time stack', 'Yalla CXO model', 'Savings unlocked'],
        'Value': [row['full_time_equivalent_cost_aed'], row['fractional_ai_solution_cost_aed'], row['estimated_annual_savings_aed']],
        'Group': ['Cost', 'Cost', 'Savings']
    })
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=52).encode(
        x=alt.X('Model:N', title=''),
        y=alt.Y('Value:Q', title='Annual AED Value'),
        color=alt.Color('Group:N', scale=alt.Scale(domain=['Cost', 'Savings'], range=[p['metric_cost'], p['metric_save']]), title=''),
        tooltip=['Model', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(df).mark_text(dy=-10, color=p['chart_text'], font='Inter', fontSize=11).encode(
        x='Model:N', y='Value:Q', text=alt.Text('Value:Q', format=',.0f')
    )
    return (bars + text).properties(title='Economic case versus full-time hiring', height=320)


def savings_trajectory_chart(row, p):
    months = list(range(1, 13))
    full_monthly = row['full_time_equivalent_cost_aed'] / 12
    yalla_monthly = row['fractional_ai_solution_cost_aed'] / 12
    data = pd.DataFrame({
        'Month': months,
        'Full-time cumulative cost': [full_monthly * m for m in months],
        'Yalla CXO cumulative cost': [yalla_monthly * m for m in months]
    })
    long = data.melt('Month', var_name='Path', value_name='Value')
    return alt.Chart(long).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('Month:O', title='Month'),
        y=alt.Y('Value:Q', title='Cumulative AED Cost'),
        color=alt.Color('Path:N', scale=alt.Scale(domain=['Full-time cumulative cost', 'Yalla CXO cumulative cost'], range=[p['danger'], p['success']]), title=''),
        tooltip=['Month', 'Path', alt.Tooltip('Value:Q', format=',.0f')]
    ).properties(title='12-month cost path comparison', height=320)


def percentile_profile_chart(filtered, row, p):
    metrics = [
        ('Savings potential', 'estimated_annual_savings_aed'),
        ('Expected ACV', 'expected_annual_contract_value_aed'),
        ('Win probability', 'win_probability'),
        ('ROI', 'expected_roi_multiple'),
        ('Urgency', 'urgency_score'),
        ('LTV', 'expected_account_ltv_aed'),
    ]
    data = []
    for label, col in metrics:
        percentile = float((filtered[col] <= row[col]).mean() * 100)
        data.append({'Metric': label, 'Percentile': percentile})
    df = pd.DataFrame(data).sort_values('Percentile', ascending=True)
    base = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X('Percentile:Q', title='Percentile within filtered portfolio', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Metric:N', sort=None, title=''),
        color=alt.condition(alt.datum.Percentile >= 75, alt.value(p['success']), alt.condition(alt.datum.Percentile >= 50, alt.value(p['accent']), alt.value(p['metric_cost']))),
        tooltip=['Metric', alt.Tooltip('Percentile:Q', format='.1f')]
    )
    rule = alt.Chart(pd.DataFrame({'x': [50]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(x='x:Q')
    text = alt.Chart(df).mark_text(align='left', dx=8, color=p['chart_text'], font='Inter', fontSize=12).encode(
        x='Percentile:Q', y=alt.Y('Metric:N', sort=None), text=alt.Text('Percentile:Q', format='.0f')
    )
    return (rule + base + text).properties(title='Descriptive profile: where this company ranks', height=300)


def company_vs_median_chart(filtered, row, p):
    metrics = [
        ('Savings index', 'estimated_annual_savings_aed'),
        ('ACV index', 'expected_annual_contract_value_aed'),
        ('ROI index', 'expected_roi_multiple'),
        ('Urgency index', 'urgency_score'),
        ('LTV index', 'expected_account_ltv_aed'),
    ]
    data = []
    for label, col in metrics:
        median = float(filtered[col].median()) if float(filtered[col].median()) != 0 else 1.0
        index_val = float(row[col]) / median * 100
        data.append({'Metric': label, 'Index': index_val})
    df = pd.DataFrame(data).sort_values('Index', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X('Index:Q', title='Company vs filtered median (median = 100)'),
        y=alt.Y('Metric:N', sort=None, title=''),
        color=alt.condition(alt.datum.Index >= 100, alt.value(p['accent_2']), alt.value(p['danger'])),
        tooltip=['Metric', alt.Tooltip('Index:Q', format='.1f')]
    )
    rule = alt.Chart(pd.DataFrame({'x': [100]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(x='x:Q')
    return (rule + bars).properties(title='Descriptive profile: company versus median account', height=300)


def need_signal_heatmap(row):
    data = [
        ('Need', 'CFO', row['cfo_need_score']),
        ('Need', 'CTO', row['cto_need_score']),
        ('Need', 'CHRO', row['chro_need_score']),
        ('Need', 'CMO', row['cmo_need_score']),
        ('Need', 'COO', row['coo_need_score']),
        ('Signal', 'Cash volatility', row['cash_flow_volatility_score']),
        ('Signal', 'Digital maturity', row['digital_maturity_score']),
        ('Signal', 'Process efficiency', row['process_efficiency_score']),
        ('Signal', 'Attrition intensity', row['attrition_rate_pct'] * 3),
        ('Signal', 'Campaign ROI signal', row['campaign_roi_x'] * 20),
        ('Signal', 'Win probability', row['win_probability'] * 100),
    ]
    df = pd.DataFrame(data, columns=['Group', 'Metric', 'Score'])
    heat = alt.Chart(df).mark_rect(cornerRadius=6).encode(
        x=alt.X('Group:N', title=''),
        y=alt.Y('Metric:N', sort=None, title=''),
        color=alt.Color('Score:Q', title='Score', scale=alt.Scale(scheme='tealblues')),
        tooltip=['Group', 'Metric', alt.Tooltip('Score:Q', format='.1f')]
    )
    text = alt.Chart(df).mark_text(font='Inter', fontSize=11).encode(
        x='Group:N', y=alt.Y('Metric:N', sort=None), text=alt.Text('Score:Q', format='.0f'),
        color=alt.condition(alt.datum.Score > 55, alt.value('white'), alt.value('#0F172A'))
    )
    return (heat + text).properties(title='Diagnostic heatmap: needs and operating signals', height=360)


def intervention_priority_chart(row, p):
    primary = row['primary_fractional_cxo']
    secondary = row['secondary_fractional_cxo']
    ai_impact = float((row['digital_maturity_score'] + row['process_efficiency_score'] + row['campaign_roi_x'] * 20) / 3)
    urgency = float(row['urgency_score'])
    close_speed = max(20, 120 - float(row['expected_close_days']))
    rows = [
        {'Action': f'{primary} engagement', 'Impact': role_score(row, primary), 'Ease': min(95, urgency * 0.6 + close_speed * 0.4), 'Priority': role_score(row, primary) * 0.7 + urgency * 0.3},
        {'Action': f'{secondary} expansion', 'Impact': role_score(row, secondary) * 0.95, 'Ease': min(90, urgency * 0.45 + 35), 'Priority': role_score(row, secondary) * 0.6 + urgency * 0.2 + 12},
        {'Action': 'AI-supported layer', 'Impact': ai_impact, 'Ease': min(92, row['digital_maturity_score'] * 0.55 + 30), 'Priority': ai_impact * 0.65 + urgency * 0.2 + row['digital_maturity_score'] * 0.15},
    ]
    df = pd.DataFrame(rows)
    scatter = alt.Chart(df).mark_circle(opacity=0.9, stroke='white', strokeWidth=1).encode(
        x=alt.X('Ease:Q', title='Ease / speed to activate', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Impact:Q', title='Expected impact', scale=alt.Scale(domain=[0, 100])),
        size=alt.Size('Priority:Q', title='Priority', scale=alt.Scale(range=[250, 1400])),
        color=alt.Color('Action:N', title=''),
        tooltip=['Action', alt.Tooltip('Impact:Q', format='.1f'), alt.Tooltip('Ease:Q', format='.1f'), alt.Tooltip('Priority:Q', format='.1f')]
    )
    labels = alt.Chart(df).mark_text(dy=-16, font='Inter', fontSize=11).encode(x='Ease:Q', y='Impact:Q', text='Action:N')
    return (scatter + labels).properties(title='Prescriptive matrix: what to do first', height=320)


def action_roadmap_chart(row, p):
    close_days = int(row['expected_close_days'])
    expansion_days = max(close_days + 30, int(row['next_service_expansion_days']))
    primary = row['primary_fractional_cxo']
    secondary = row['secondary_fractional_cxo']
    roadmap = pd.DataFrame([
        {'Stage': 'Pitch and diagnose', 'Start': 0, 'End': max(10, min(14, close_days // 2 if close_days > 1 else 7)), 'Owner': 'Commercial'},
        {'Stage': 'Close and onboard', 'Start': max(10, min(14, close_days // 2 if close_days > 1 else 7)), 'End': close_days, 'Owner': 'Commercial'},
        {'Stage': f'Activate {primary}', 'Start': close_days, 'End': close_days + 30, 'Owner': primary},
        {'Stage': 'Deploy AI operating layer', 'Start': close_days + 15, 'End': close_days + 45, 'Owner': 'AI layer'},
        {'Stage': f'Expand into {secondary}', 'Start': close_days + 35, 'End': expansion_days, 'Owner': secondary},
    ])
    bars = alt.Chart(roadmap).mark_bar(cornerRadius=8, height=22).encode(
        x=alt.X('Start:Q', title='Days from today'),
        x2='End:Q',
        y=alt.Y('Stage:N', sort=None, title=''),
        color=alt.Color('Owner:N', title=''),
        tooltip=['Stage', 'Owner', 'Start', 'End']
    )
    rules = alt.Chart(pd.DataFrame({'x': [close_days, expansion_days]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(x='x:Q')
    return (rules + bars).properties(title='Prescriptive roadmap: close, land, expand', height=280)


def peer_position_chart(filtered, row, p):
    peers = filtered.copy()
    peers['selected'] = peers['company_name'].eq(row['company_name'])
    x_mid = peers['estimated_annual_savings_aed'].median()
    y_mid = peers['expected_annual_contract_value_aed'].median()
    rules_x = alt.Chart(pd.DataFrame({'x': [x_mid]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(x='x:Q')
    rules_y = alt.Chart(pd.DataFrame({'y': [y_mid]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(y='y:Q')
    base = alt.Chart(peers).mark_circle(opacity=0.78, stroke='white', strokeWidth=0.6).encode(
        x=alt.X('estimated_annual_savings_aed:Q', title='Estimated annual savings (AED)'),
        y=alt.Y('expected_annual_contract_value_aed:Q', title='Expected ACV (AED)'),
        size=alt.Size('win_probability:Q', title='Win probability', scale=alt.Scale(range=[70, 900])),
        color=alt.condition(alt.datum.selected, alt.value(p['danger']), alt.Color('primary_fractional_cxo:N', title='Primary CXO')),
        tooltip=['company_name', 'sector', 'primary_fractional_cxo', 'secondary_fractional_cxo', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability']
    )
    label = alt.Chart(peers[peers['selected']]).mark_text(dx=8, dy=-8, color=p['chart_text'], font='Inter', fontSize=11).encode(
        x='estimated_annual_savings_aed:Q', y='expected_annual_contract_value_aed:Q', text='company_name:N'
    )
    return (rules_x + rules_y + base + label).properties(title='Portfolio context: position of selected company', height=360)


def comparable_accounts(filtered, row):
    subset = filtered.copy()
    subset['distance'] = ((subset['revenue_aed_bn'] - row['revenue_aed_bn']).abs() * 2 + (subset['urgency_score'] - row['urgency_score']).abs() * 0.45 + (subset['expected_annual_contract_value_aed'] - row['expected_annual_contract_value_aed']).abs() / 500000)
    subset = subset[subset['company_name'] != row['company_name']].sort_values('distance').head(5)
    out = subset[['company_name', 'sector', 'primary_fractional_cxo', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability']].copy()
    out['estimated_annual_savings_aed'] = out['estimated_annual_savings_aed'].map(fmt_aed)
    out['expected_annual_contract_value_aed'] = out['expected_annual_contract_value_aed'].map(fmt_aed)
    out['win_probability'] = (out['win_probability'] * 100).round(1).astype(str) + '%'
    return out.rename(columns={'company_name': 'Comparable company', 'sector': 'Sector', 'primary_fractional_cxo': 'Primary CXO', 'estimated_annual_savings_aed': 'Savings', 'expected_annual_contract_value_aed': 'Expected ACV', 'win_probability': 'Win Prob.'})


def recommendation_text(row, filtered):
    role_subset = filtered[filtered['primary_fractional_cxo'] == row['primary_fractional_cxo']]
    role_avg_save = role_subset['estimated_annual_savings_aed'].mean()
    sector_pipeline = filtered[filtered['sector'] == row['sector']]['weighted_pipeline_value_aed'].sum()
    return {
        'lead': f"Lead with a {row['primary_fractional_cxo']}-first conversation because that is the highest modeled pain point for {row['company_name']}. Position {row['secondary_fractional_cxo']} as the next expansion layer once the first intervention proves value.",
        'economics': f"The commercial anchor is the savings gap: {fmt_aed(row['full_time_equivalent_cost_aed'])} under a full-time executive structure versus {fmt_aed(row['fractional_ai_solution_cost_aed'])} through Yalla CXO, creating {fmt_aed(row['estimated_annual_savings_aed'])} in annual savings.",
        'timing': f"This account has a {row['win_probability'] * 100:.1f}% modeled win probability and an expected close horizon of {int(row['expected_close_days'])} days, so it should be treated as a live opportunity rather than a distant prospect.",
        'benchmark': f"Within the current filtered portfolio, companies with a primary {row['primary_fractional_cxo']} recommendation average {fmt_aed(role_avg_save)} in modeled savings. That makes this role-led pitch commercially credible, not hypothetical.",
        'sector': f"{row['sector']} contributes {fmt_aed(sector_pipeline)} in weighted pipeline value within the selected portfolio, so this company can be used as a sector-specific proof point during broader business development.",
        'upsell': f"After the primary engagement, the best expansion path is {row['secondary_fractional_cxo']} plus AI-supported roles: {row['ai_supported_roles']}. The modeled next-service expansion window is {int(row['next_service_expansion_days'])} days."
    }


def profile_shell(row):
    badges = ''.join([
        f"<div class='badge-pill'>Sector · {row['sector']}</div>",
        f"<div class='badge-pill'>Revenue band · {row['revenue_band']}</div>",
        f"<div class='badge-pill'>Account tier · {row['account_tier']}</div>",
        f"<div class='badge-pill'>Urgency · {row['urgency_tier']} ({row['urgency_score']:.1f})</div>",
        f"<div class='badge-pill'>Service mix · {row['service_mix']}</div>",
    ])
    stats_html = (
        "<div class='mini-stat-grid'>"
        f"<div class='mini-stat'><div class='label'>Primary CXO</div><div class='value'>{row['primary_fractional_cxo']}</div><div class='sub'>Lead recommendation for first engagement.</div></div>"
        f"<div class='mini-stat'><div class='label'>Secondary CXO</div><div class='value'>{row['secondary_fractional_cxo']}</div><div class='sub'>Best expansion role after the first intervention.</div></div>"
        f"<div class='mini-stat'><div class='label'>Expected LTV</div><div class='value'>{fmt_aed(row['expected_account_ltv_aed'])}</div><div class='sub'>Longer-term account value if the relationship expands well.</div></div>"
        f"<div class='mini-stat'><div class='label'>Best next action</div><div class='value'>{row['ideal_next_action']}</div><div class='sub'>Recommended commercial move for this account.</div></div>"
        "</div>"
    )
    html = (
        "<div class='glass-card'>"
        "<div class='section-kicker'>Selected company</div>"
        f"<div class='section-title'>{row['company_name']}</div>"
        "<div class='section-copy'>This view is designed to help you pitch one company at a time by showing descriptive profile, diagnostic evidence, prescriptive action sequence, and broader portfolio position in one flow.</div>"
        f"<div class='badge-row'>{badges}</div>"
        f"{stats_html}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def selector_banner(row, idx, total):
    st.markdown(
        f"<div class='company-shell'><div class='company-head'><div><div class='section-kicker'>Pitch target</div><div class='company-title'>{row['company_name']}</div><div class='company-sub'>You are viewing company {idx+1} of {total}. The tabs below now separate descriptive, diagnostic, and prescriptive visuals so every company can be pitched with a clearer storyline.</div></div><div class='mode-pill'>Primary focus · {row['primary_fractional_cxo']}</div></div></div>",
        unsafe_allow_html=True,
    )


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


df = load_data()
init_state(df)
palette = get_palette(st.session_state.appearance_mode)
enable_altair_theme(palette)
inject_css(palette)

st.markdown(f"<div class='hero-shell'><div class='hero-top'><div><div class='hero-title'>Yalla CXO</div><div class='hero-sub'>Company-first pitching dashboard with richer Altair storytelling: descriptive context, diagnostic evidence, prescriptive action, and portfolio positioning for every target account.</div></div><div class='mode-pill'>{st.session_state.appearance_mode} mode</div></div></div>", unsafe_allow_html=True)

with st.expander('Pitch setup: company selection, filters, and appearance', expanded=False):
    st.markdown("<div class='setup-shell'><div class='setup-head'><div><div class='setup-title'>Pitch setup</div><div class='setup-copy'>Adjust appearance, narrow the account universe, and choose the company you want to pitch. Keep this panel collapsed during presentations for a cleaner view.</div></div></div></div>", unsafe_allow_html=True)
    top_a, top_b, top_c = st.columns([1.25, 0.55, 0.55], gap='large')
    with top_a:
        company_options = sorted(df['company_name'].tolist())
        setup_index = company_options.index(st.session_state.selected_company) if st.session_state.selected_company in company_options else 0
        setup_company = st.selectbox('Company to pitch', company_options, index=setup_index, key='setup_selected_company')
        if setup_company != st.session_state.selected_company:
            st.session_state.selected_company = setup_company
    with top_b:
        light_toggle = st.toggle('Light mode', value=st.session_state.appearance_mode == 'Light')
        st.session_state.appearance_mode = 'Light' if light_toggle else 'Dark'
    with top_c:
        if st.button('Reset all filters', use_container_width=True):
            reset_filters(df)
            st.rerun()
    f1, f2, f3, f4 = st.columns(4, gap='large')
    with f1:
        st.multiselect('Sector', sorted(df['sector'].unique()), key='flt_sector')
    with f2:
        st.multiselect('Primary CXO', sorted(df['primary_fractional_cxo'].unique()), key='flt_role')
    with f3:
        st.multiselect('Urgency Tier', sorted(df['urgency_tier'].unique()), key='flt_urgency')
    with f4:
        st.multiselect('Account Tier', sorted(df['account_tier'].unique()), key='flt_tier')
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

sel_col, nav_prev, nav_next = st.columns([6.5, 0.8, 0.8], gap='medium')
with sel_col:
    st.selectbox('Selected company', available_companies, key='selected_company', label_visibility='collapsed')
current_idx = available_companies.index(st.session_state.selected_company)
with nav_prev:
    if st.button('◀', use_container_width=True, disabled=current_idx == 0):
        st.session_state.selected_company = available_companies[current_idx - 1]
        st.rerun()
with nav_next:
    if st.button('▶', use_container_width=True, disabled=current_idx == len(available_companies) - 1):
        st.session_state.selected_company = available_companies[current_idx + 1]
        st.rerun()

row = filtered.loc[filtered['company_name'] == st.session_state.selected_company].iloc[0]
texts = recommendation_text(row, filtered)
selector_banner(row, current_idx, len(available_companies))
profile_shell(row)

c1, c2, c3, c4, c5 = st.columns(5, gap='medium')
with c1:
    kpi_card('Annual savings', fmt_aed(row['estimated_annual_savings_aed']), 'Modeled cost reduction versus full-time executive hiring.')
with c2:
    kpi_card('Expected ACV', fmt_aed(row['expected_annual_contract_value_aed']), 'Projected annual contract value if this account converts.')
with c3:
    kpi_card('Win probability', f"{row['win_probability']*100:.1f}%", 'Commercial likelihood based on stage, urgency, and account attractiveness.')
with c4:
    kpi_card('Expected ROI', f"{row['expected_roi_multiple']:.2f}x", 'Estimated return multiple for the client on the proposed model.')
with c5:
    kpi_card('Close horizon', f"{int(row['expected_close_days'])} days", 'Modeled time to close given current pipeline conditions.')

callout(f"<strong>Pitch recommendation for {row['company_name']}:</strong> {texts['lead']} {texts['economics']}")

tab1, tab2, tab3, tab4 = st.tabs(['Descriptive', 'Diagnostic', 'Prescriptive', 'Portfolio'])

with tab1:
    section_header('Descriptive', 'Show what this company looks like before you explain why it matters', 'These visuals locate the company inside the filtered portfolio and frame its commercial profile before you move into diagnosis or action.')
    a, b = st.columns(2, gap='large')
    with a:
        st.altair_chart(percentile_profile_chart(filtered, row, palette), use_container_width=True)
    with b:
        st.altair_chart(company_vs_median_chart(filtered, row, palette), use_container_width=True)
    c, d = st.columns(2, gap='large')
    with c:
        st.altair_chart(company_cost_chart(row, palette), use_container_width=True)
    with d:
        st.altair_chart(savings_trajectory_chart(row, palette), use_container_width=True)
    i1, i2 = st.columns(2, gap='large')
    with i1:
        insight_card('Commercial summary', texts['economics'])
    with i2:
        insight_card('Why this account stands out', f"This company sits at percentile-led positions across savings, ACV, ROI, urgency, and LTV, giving you a factual way to explain why it deserves time now.")

with tab2:
    section_header('Diagnostic', 'Explain the underlying business problem', 'These charts connect executive need, operating friction, and account readiness so the recommendation feels evidence-based rather than generic.')
    a, b = st.columns([0.52, 0.48], gap='large')
    with a:
        st.altair_chart(role_profile_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(operating_signal_chart(row), use_container_width=True)
    st.altair_chart(need_signal_heatmap(row), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Primary recommendation', texts['lead'])
    with i2:
        insight_card('Why now', texts['timing'])
    with i3:
        insight_card('Expansion logic', texts['upsell'])

with tab3:
    section_header('Prescriptive', 'Show the next best actions, not just the diagnosis', 'These visuals turn the analysis into a delivery sequence by ranking interventions and showing a realistic land-and-expand path.')
    a, b = st.columns([0.52, 0.48], gap='large')
    with a:
        st.altair_chart(intervention_priority_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(action_roadmap_chart(row, palette), use_container_width=True)
    i1, i2 = st.columns(2, gap='large')
    with i1:
        insight_card('Recommended sequencing', f"Start with {row['primary_fractional_cxo']} because it is the strongest modeled need. Use the early proof window to validate value, then introduce the AI-supported layer and {row['secondary_fractional_cxo']} expansion.")
    with i2:
        insight_card('Prescriptive logic', texts['benchmark'])

with tab4:
    section_header('Positioning', 'Place the account inside the wider pipeline', 'This final section shows whether the selected company is a balanced opportunity or an outlier versus the rest of the filtered portfolio.')
    a, b = st.columns([0.58, 0.42], gap='large')
    with a:
        st.altair_chart(peer_position_chart(filtered, row, palette), use_container_width=True)
    with b:
        insight_card('Sector proof point', texts['sector'])
        insight_card('Meeting talk track', f"Open with the {row['primary_fractional_cxo']}-led pain, quantify the {fmt_aed(row['estimated_annual_savings_aed'])} savings gap, then position {row['secondary_fractional_cxo']} and the AI-supported operating layer as the low-friction expansion path.")
    st.subheader('Closest comparable accounts')
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
