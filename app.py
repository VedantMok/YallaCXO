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
            "bg": "#F5F7FB", "bg_grad_1": "rgba(61,131,255,0.08)", "bg_grad_2": "rgba(16,185,129,0.08)",
            "panel": "rgba(255,255,255,0.84)", "panel_solid": "#FFFFFF", "border": "rgba(15,23,42,0.08)",
            "text": "#102033", "muted": "#5E738A", "accent": "#2563EB", "accent_2": "#14B8A6",
            "accent_3": "#7C3AED", "success": "#10B981", "danger": "#F97316", "pill_bg": "rgba(37,99,235,0.06)",
            "callout_start": "rgba(37,99,235,0.08)", "callout_end": "rgba(20,184,166,0.08)", "chart_text": "#102033",
            "chart_label": "#4B6075", "chart_grid": "rgba(15,23,42,0.08)", "hero_start": "#EAF2FF", "hero_mid": "#F7FBFF",
            "hero_end": "#EEFFFB", "shadow": "0 16px 40px rgba(15,23,42,0.08)", "metric_cost": "#64748B", "metric_save": "#10B981",
            "highlight": "#2563EB",
        }
    return {
        "bg": "#0B1220", "bg_grad_1": "rgba(37,99,235,0.12)", "bg_grad_2": "rgba(20,184,166,0.10)",
        "panel": "rgba(15,23,42,0.74)", "panel_solid": "#111827", "border": "rgba(148,163,184,0.14)",
        "text": "#E8EEF8", "muted": "#9FB0C5", "accent": "#60A5FA", "accent_2": "#2DD4BF",
        "accent_3": "#A78BFA", "success": "#34D399", "danger": "#FB923C", "pill_bg": "rgba(96,165,250,0.08)",
        "callout_start": "rgba(96,165,250,0.10)", "callout_end": "rgba(45,212,191,0.10)", "chart_text": "#E8EEF8",
        "chart_label": "#AFC0D6", "chart_grid": "rgba(148,163,184,0.12)", "hero_start": "#0F172A", "hero_mid": "#111827",
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
        alt.themes.register("yalla_theme_with_lens", theme)
    except Exception:
        pass
    alt.themes.enable("yalla_theme_with_lens")


def inject_css(p):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
    html, body, [class*="css"] {{font-family: 'Inter', sans-serif;}}
    .stApp {{background: radial-gradient(circle at 10% 20%, {p['bg_grad_1']}, transparent 28%), radial-gradient(circle at 90% 10%, {p['bg_grad_2']}, transparent 25%), linear-gradient(180deg, {p['bg']} 0%, {p['bg']} 100%); color: {p['text']};}}
    .block-container {{padding-top: 1.08rem; padding-bottom: 2rem; max-width: 1420px;}}
    section[data-testid="stSidebar"] {{display:none;}}
    .hero-shell {{background: linear-gradient(135deg, {p['hero_start']} 0%, {p['hero_mid']} 55%, {p['hero_end']} 100%); border: 1px solid {p['border']}; border-radius: 28px; padding: 1.55rem 1.75rem 1.35rem 1.75rem; box-shadow: {p['shadow']}; margin-bottom: 1rem; position: relative; overflow: hidden;}}
    .hero-shell:before {{content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent); transform: translateX(-100%); animation: shimmer 8s infinite linear;}}
    @keyframes shimmer {{100% {{transform: translateX(100%);}}}}
    .hero-top {{display:flex; align-items:flex-start; justify-content:space-between; gap:1rem;}}
    .hero-title {{font-family:'Space Grotesk',sans-serif; font-size:2.28rem; font-weight:700; margin:0; color:{p['text']};}}
    .hero-sub {{margin-top:.42rem; color:{p['muted']}; max-width:980px; line-height:1.6; font-size:1rem;}}
    .mode-pill {{display:inline-flex; padding:.45rem .75rem; border-radius:999px; background:{p['pill_bg']}; border:1px solid {p['border']}; color:{p['text']}; font-size:.82rem;}}
    .glass-card {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:24px; padding:1.35rem; box-shadow:{p['shadow']}; backdrop-filter:blur(12px); margin-bottom:1rem;}}
    .company-shell {{background: linear-gradient(135deg, {p['callout_start']} 0%, {p['callout_end']} 100%); border:1px solid {p['border']}; border-radius:22px; padding:1.15rem 1.2rem; box-shadow:{p['shadow']}; margin-bottom:1rem;}}
    .company-head {{display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;}}
    .company-title {{font-family:'Space Grotesk',sans-serif; font-size:1.55rem; color:{p['text']}; margin:0;}}
    .company-sub {{color:{p['muted']}; margin-top:.2rem; line-height:1.55; max-width:780px;}}
    .badge-row {{display:flex; gap:.6rem; flex-wrap:wrap; margin:.95rem 0 1.05rem 0;}}
    .badge-pill {{display:inline-flex; align-items:center; gap:.4rem; padding:.5rem .82rem; background:{p['pill_bg']}; color:{p['text']}; border:1px solid {p['border']}; border-radius:999px; font-size:.83rem; line-height:1;}}
    .section-kicker {{font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:{p['accent_2']}; margin-bottom:.32rem;}}
    .section-title {{font-family:'Space Grotesk',sans-serif; color:{p['text']}; font-size:1.38rem; margin:.1rem 0 .18rem 0;}}
    .section-copy {{color:{p['muted']}; line-height:1.58; margin-bottom:.95rem;}}
    .kpi-card {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; padding:1rem .95rem .92rem .95rem; min-height:126px; box-shadow:{p['shadow']};}}
    .kpi-label {{font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; color:{p['muted']}; margin-bottom:.34rem;}}
    .kpi-value {{font-family:'Space Grotesk',sans-serif; font-size:1.52rem; font-weight:700; color:{p['text']}; margin-bottom:.26rem; line-height:1.1;}}
    .kpi-sub {{font-size:.84rem; color:{p['muted']}; line-height:1.45;}}
    .mini-stat-grid {{display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:.85rem; margin-top:.3rem;}}
    .mini-stat {{background:{p['pill_bg']}; border:1px solid {p['border']}; border-radius:18px; padding:.95rem 1rem; min-height:104px;}}
    .mini-stat .label {{color:{p['muted']}; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em;}}
    .mini-stat .value {{font-family:'Space Grotesk',sans-serif; color:{p['text']}; font-size:1.15rem; margin-top:.22rem;}}
    .mini-stat .sub {{color:{p['muted']}; font-size:.82rem; margin-top:.22rem; line-height:1.45;}}
    .callout-box {{background: linear-gradient(135deg, {p['callout_start']} 0%, {p['callout_end']} 100%); border:1px solid {p['border']}; border-left:4px solid {p['highlight']}; border-radius:22px; padding:1rem 1.1rem; margin:.8rem 0 1.1rem 0; box-shadow:{p['shadow']}; line-height:1.6; color:{p['text']};}}
    .insight-box {{background:{p['panel']}; border:1px solid {p['border']}; border-left:4px solid {p['accent']}; border-radius:18px; padding:1rem 1.02rem; box-shadow:{p['shadow']}; height:100%;}}
    .insight-box h4 {{margin:0 0 .45rem 0; color:{p['text']}; font-size:1rem;}}
    .insight-box p {{margin:0; color:{p['muted']}; line-height:1.56;}}
    .stTabs [data-baseweb="tab-list"] {{gap:.55rem; margin-bottom:.4rem;}}
    .stTabs [data-baseweb="tab"] {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:14px; color:{p['muted']}; padding:.6rem 1rem;}}
    .stTabs [aria-selected="true"] {{background: linear-gradient(180deg, {p['callout_start']}, {p['callout_end']}); color:{p['text']}; border-color:{p['highlight']};}}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{background:{p['panel']}; border-color:{p['border']};}}
    div[data-testid="stDataFrame"] {{border:1px solid {p['border']}; border-radius:18px; overflow:hidden;}}
    details {{background:{p['panel']}; border:1px solid {p['border']}; border-radius:22px; box-shadow:{p['shadow']};}}
    details summary {{padding:.95rem 1rem;}}
    @media (max-width:1100px) {{.mini-stat-grid {{grid-template-columns:1fr 1fr;}} .hero-title {{font-size:1.9rem;}} .hero-top {{flex-direction:column;}}}}
    @media (max-width:760px) {{.mini-stat-grid {{grid-template-columns:1fr;}} .company-head {{flex-direction:column;}}}}
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


def role_profile_chart(row, p):
    df = pd.DataFrame({'Role': ['CFO', 'CTO', 'CHRO', 'CMO', 'COO'], 'Need Score': [row['cfo_need_score'], row['cto_need_score'], row['chro_need_score'], row['cmo_need_score'], row['coo_need_score']]}).sort_values('Need Score', ascending=True)
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(x=alt.X('Need Score:Q', title='Need Score', scale=alt.Scale(domain=[0, 100])), y=alt.Y('Role:N', sort=None, title=''), color=alt.Color('Role:N', title=''), tooltip=['Role', 'Need Score'])
    text = alt.Chart(df).mark_text(align='left', dx=8, color=p['chart_text'], font='Inter', fontSize=12).encode(x='Need Score:Q', y=alt.Y('Role:N', sort=None), text=alt.Text('Need Score:Q', format='.1f'))
    return (bars + text).properties(title='Role fit and recommendation strength', height=300)


def company_cost_chart(row, p):
    df = pd.DataFrame({'Model': ['Full-time executive stack', 'Yalla CXO hybrid model', 'Annual savings unlocked'], 'Value': [row['full_time_equivalent_cost_aed'], row['fractional_ai_solution_cost_aed'], row['estimated_annual_savings_aed']], 'Group': ['Cost', 'Cost', 'Savings']})
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=52).encode(x=alt.X('Model:N', title=''), y=alt.Y('Value:Q', title='Annual AED Value'), color=alt.Color('Group:N', scale=alt.Scale(domain=['Cost', 'Savings'], range=[p['metric_cost'], p['metric_save']]), title=''), tooltip=['Model', alt.Tooltip('Value:Q', format=',.0f')])
    text = alt.Chart(df).mark_text(dy=-10, color=p['chart_text'], font='Inter', fontSize=11).encode(x='Model:N', y='Value:Q', text=alt.Text('Value:Q', format=',.0f'))
    return (bars + text).properties(title='Economic case versus full-time hiring', height=320)


def operating_signal_chart(row):
    signals = pd.DataFrame({'Signal': ['Cash volatility', 'Digital maturity', 'Process efficiency', 'Attrition', 'Campaign ROI', 'Win probability'], 'Value': [row['cash_flow_volatility_score'], row['digital_maturity_score'], row['process_efficiency_score'], row['attrition_rate_pct'] * 3, row['campaign_roi_x'] * 20, row['win_probability'] * 100], 'Category': ['Finance', 'Technology', 'Operations', 'People', 'Growth', 'Commercial']}).sort_values('Value', ascending=True)
    return alt.Chart(signals).mark_bar(cornerRadiusEnd=10, height=22).encode(x=alt.X('Value:Q', title='Scaled score / intensity'), y=alt.Y('Signal:N', sort=None, title=''), color=alt.Color('Category:N', title=''), tooltip=['Signal', 'Category', alt.Tooltip('Value:Q', format='.1f')]).properties(title='Operating signal snapshot', height=300)


def peer_position_chart(filtered, row, p):
    peers = filtered.copy()
    peers['selected'] = peers['company_name'].eq(row['company_name'])
    x_mid = peers['estimated_annual_savings_aed'].median()
    y_mid = peers['expected_annual_contract_value_aed'].median()
    rules_x = alt.Chart(pd.DataFrame({'x': [x_mid]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(x='x:Q')
    rules_y = alt.Chart(pd.DataFrame({'y': [y_mid]})).mark_rule(strokeDash=[6, 6], color=p['chart_grid']).encode(y='y:Q')
    base = alt.Chart(peers).mark_circle(opacity=0.78, stroke='white', strokeWidth=0.6).encode(x=alt.X('estimated_annual_savings_aed:Q', title='Estimated Annual Savings (AED)'), y=alt.Y('expected_annual_contract_value_aed:Q', title='Expected ACV (AED)'), size=alt.Size('win_probability:Q', title='Win Probability', scale=alt.Scale(range=[70, 900])), color=alt.condition(alt.datum.selected, alt.value(p['danger']), alt.Color('primary_fractional_cxo:N', title='Primary CXO')), tooltip=['company_name', 'sector', 'primary_fractional_cxo', 'secondary_fractional_cxo', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability'])
    label = alt.Chart(peers[peers['selected']]).mark_text(dx=8, dy=-8, color=p['chart_text'], font='Inter', fontSize=11).encode(x='estimated_annual_savings_aed:Q', y='expected_annual_contract_value_aed:Q', text='company_name:N')
    return (rules_x + rules_y + base + label).properties(title='Portfolio position of the selected company', height=360)


def savings_trajectory_chart(row, p):
    months = list(range(1, 13))
    full_monthly = row['full_time_equivalent_cost_aed'] / 12
    yalla_monthly = row['fractional_ai_solution_cost_aed'] / 12
    data = pd.DataFrame({'Month': months, 'Full-time cumulative cost': [full_monthly * m for m in months], 'Yalla CXO cumulative cost': [yalla_monthly * m for m in months]})
    long = data.melt('Month', var_name='Path', value_name='Value')
    return alt.Chart(long).mark_line(point=True, strokeWidth=3).encode(x=alt.X('Month:O', title='Month'), y=alt.Y('Value:Q', title='Cumulative AED Cost'), color=alt.Color('Path:N', scale=alt.Scale(domain=['Full-time cumulative cost', 'Yalla CXO cumulative cost'], range=[p['danger'], p['success']]), title=''), tooltip=['Month', 'Path', alt.Tooltip('Value:Q', format=',.0f')]).properties(title='12-month cost path comparison', height=320)


def descriptive_benchmark_chart(filtered, row, p):
    metrics = [
        ('Annual savings', 'estimated_annual_savings_aed'),
        ('Expected ACV', 'expected_annual_contract_value_aed'),
        ('Expected LTV', 'expected_account_ltv_aed'),
        ('Win probability', 'win_probability'),
        ('ROI multiple', 'expected_roi_multiple'),
        ('Urgency score', 'urgency_score')
    ]
    rows = []
    for label, col in metrics:
        median = filtered[col].median()
        company = row[col]
        company_idx = 100 if median == 0 else min(220, company / median * 100)
        rows.append({'Metric': label, 'Series': 'Portfolio median', 'Index': 100})
        rows.append({'Metric': label, 'Series': 'Selected company', 'Index': company_idx})
    df = pd.DataFrame(rows)
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('Metric:N', title=''),
        y=alt.Y('Index:Q', title='Index vs portfolio median (100 = median)'),
        color=alt.Color('Series:N', scale=alt.Scale(domain=['Portfolio median', 'Selected company'], range=[p['metric_cost'], p['accent']]), title=''),
        xOffset='Series:N',
        tooltip=['Metric', 'Series', alt.Tooltip('Index:Q', format='.1f')]
    )
    return chart.properties(title='Descriptive: how this company compares with the filtered portfolio', height=340)


def diagnostic_gap_chart(filtered, row, p):
    mapping = {
        'CFO': 'cfo_need_score',
        'CTO': 'cto_need_score',
        'CHRO': 'chro_need_score',
        'CMO': 'cmo_need_score',
        'COO': 'coo_need_score'
    }
    rows = []
    for role, col in mapping.items():
        delta = row[col] - filtered[col].mean()
        rows.append({'Role': role, 'Gap': delta})
    df = pd.DataFrame(rows).sort_values('Gap')
    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=8).encode(
        x=alt.X('Gap:Q', title='Need-score gap vs filtered portfolio average'),
        y=alt.Y('Role:N', sort=None, title=''),
        color=alt.condition(alt.datum.Gap > 0, alt.value(p['accent']), alt.value(p['danger'])),
        tooltip=['Role', alt.Tooltip('Gap:Q', format='.1f')]
    )
    rule = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color=p['chart_grid']).encode(x='x:Q')
    text = alt.Chart(df).mark_text(dx=8, color=p['chart_text'], font='Inter', fontSize=12).encode(x='Gap:Q', y=alt.Y('Role:N', sort=None), text=alt.Text('Gap:Q', format='.1f'))
    return (rule + bars + text).properties(title='Diagnostic: which role needs are above or below portfolio norm', height=320)


def prescriptive_action_chart(row, p):
    role_map = {'CFO': row['cfo_need_score'], 'CTO': row['cto_need_score'], 'CHRO': row['chro_need_score'], 'CMO': row['cmo_need_score'], 'COO': row['coo_need_score']}
    primary = row['primary_fractional_cxo']
    secondary = row['secondary_fractional_cxo']
    primary_score = role_map.get(primary, 0)
    secondary_score = role_map.get(secondary, 0)
    expansion_speed = max(0, 100 - min(100, row['next_service_expansion_days'] / 2))
    actions = pd.DataFrame([
        {'Action': f'Lead with {primary}', 'Priority': min(100, primary_score * 0.75 + row['urgency_score'] * 0.25), 'Anchor': row['expected_annual_contract_value_aed'], 'Type': 'Primary pitch'},
        {'Action': 'Push proposal / pilot', 'Priority': min(100, row['win_probability'] * 100 * 0.7 + row['urgency_score'] * 0.3), 'Anchor': row['weighted_pipeline_value_aed'], 'Type': 'Conversion'},
        {'Action': f'Expand into {secondary}', 'Priority': min(100, secondary_score * 0.7 + expansion_speed * 0.3), 'Anchor': max(0, row['expected_account_ltv_aed'] - row['expected_annual_contract_value_aed']), 'Type': 'Upsell'},
        {'Action': 'Bundle AI add-ons', 'Priority': min(100, 45 + row['expected_roi_multiple'] * 12 + row['estimated_savings_pct'] * 0.35), 'Anchor': row['estimated_annual_savings_aed'], 'Type': 'Efficiency'}
    ]).sort_values('Priority')
    bars = alt.Chart(actions).mark_bar(cornerRadiusEnd=10, height=24).encode(
        x=alt.X('Priority:Q', title='Recommended action priority score'),
        y=alt.Y('Action:N', sort=None, title=''),
        color=alt.Color('Type:N', title=''),
        tooltip=['Action', 'Type', alt.Tooltip('Priority:Q', format='.1f'), alt.Tooltip('Anchor:Q', format=',.0f')]
    )
    text = alt.Chart(actions).mark_text(dx=8, color=p['chart_text'], font='Inter', fontSize=12).encode(x='Priority:Q', y=alt.Y('Action:N', sort=None), text=alt.Text('Priority:Q', format='.0f'))
    return (bars + text).properties(title='Prescriptive: what to do next and in what order', height=320)


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
        "<div class='section-copy'>This view is designed to help you pitch one company at a time by showing its executive need profile, cost advantage, portfolio position, and expansion path in a single narrative flow.</div>"
        f"<div class='badge-row'>{badges}</div>"
        f"{stats_html}"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def selector_banner(row, idx, total):
    st.markdown(f"<div class='company-shell'><div class='company-head'><div><div class='section-kicker'>Pitch target</div><div class='company-title'>{row['company_name']}</div><div class='company-sub'>You are viewing company {idx+1} of {total}. Use the company picker or previous/next buttons to move through targets quickly. The setup panel above controls appearance and portfolio filters.</div></div><div class='mode-pill'>Primary focus · {row['primary_fractional_cxo']}</div></div></div>", unsafe_allow_html=True)


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

st.markdown(f"<div class='hero-shell'><div class='hero-top'><div><div class='hero-title'>Yalla CXO</div><div class='hero-sub'>Company-first pitching dashboard with descriptive, diagnostic, and prescriptive data views that help explain what the numbers say, why they look that way, and what to do next.</div></div><div class='mode-pill'>{st.session_state.appearance_mode} mode</div></div></div>", unsafe_allow_html=True)

initial_mode = st.session_state.appearance_mode
with st.expander('Pitch setup: company selection, filters, and appearance', expanded=False):
    top_a, top_b, top_c = st.columns([1.25, 0.55, 0.55], gap='large')
    with top_a:
        st.selectbox('Company to pitch', sorted(df['company_name'].tolist()), key='selected_company')
    with top_b:
        light_toggle = st.toggle('Light mode', value=initial_mode == 'Light')
        new_mode = 'Light' if light_toggle else 'Dark'
        if new_mode != initial_mode:
            st.session_state.appearance_mode = new_mode
            st.rerun()
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

tab1, tab2, tab3, tab4 = st.tabs(['Recommendation', 'Economics', 'Portfolio Context', 'Data Lens'])
with tab1:
    section_header('Diagnostic', 'Lead with the right executive problem', 'This section makes the recommendation feel evidence-based by showing the dominant executive need and the operating signals that support it.')
    a, b = st.columns([0.55, 0.45], gap='large')
    with a:
        st.altair_chart(role_profile_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(operating_signal_chart(row), use_container_width=True)
    i1, i2, i3 = st.columns(3, gap='large')
    with i1:
        insight_card('Primary recommendation', texts['lead'])
    with i2:
        insight_card('Why now', texts['timing'])
    with i3:
        insight_card('Expansion logic', texts['upsell'])

with tab2:
    section_header('Economics', 'Make the savings case obvious', 'This section compares full-time executive cost versus the Yalla CXO hybrid model, then shows how the cost path diverges over 12 months.')
    a, b = st.columns(2, gap='large')
    with a:
        st.altair_chart(company_cost_chart(row, palette), use_container_width=True)
    with b:
        st.altair_chart(savings_trajectory_chart(row, palette), use_container_width=True)
    i1, i2 = st.columns(2, gap='large')
    with i1:
        insight_card('Economic justification', texts['economics'])
    with i2:
        insight_card('Role benchmark', texts['benchmark'])

with tab3:
    section_header('Positioning', 'Show where this company sits in the broader opportunity map', 'This section shows whether the selected company is a standout savings case, a standout revenue case, or a balanced priority versus comparable accounts.')
    a, b = st.columns([0.58, 0.42], gap='large')
    with a:
        st.altair_chart(peer_position_chart(filtered, row, palette), use_container_width=True)
    with b:
        insight_card('Sector proof point', texts['sector'])
        insight_card('Meeting talk track', f"Open with the {row['primary_fractional_cxo']}-led pain, quantify the {fmt_aed(row['estimated_annual_savings_aed'])} savings gap, then position {row['secondary_fractional_cxo']} and the AI-supported operating layer as the low-friction expansion path.")
    st.subheader('Closest comparable accounts')
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

with tab4:
    section_header('Data visualization', 'Use descriptive, diagnostic, and prescriptive views to explain the numbers', 'These views are designed to make the dataset easier to narrate in a pitch. Descriptive shows what the company looks like, diagnostic shows what is driving the pattern, and prescriptive shows what should be done next.')
    lens1, lens2, lens3 = st.tabs(['Descriptive', 'Diagnostic', 'Prescriptive'])
    with lens1:
        a, b = st.columns([0.64, 0.36], gap='large')
        with a:
            st.altair_chart(descriptive_benchmark_chart(filtered, row, palette), use_container_width=True)
        with b:
            insight_card('How to read this', 'Each metric is indexed against the filtered portfolio median, where 100 equals the median. Values above 100 mean this company is stronger or more intense than the typical account in the current selection.')
            insight_card('What it says here', f"This company stands out where the index is highest. Use those above-median metrics to explain why it deserves attention relative to the rest of the filtered account list.")
    with lens2:
        a, b = st.columns([0.6, 0.4], gap='large')
        with a:
            st.altair_chart(diagnostic_gap_chart(filtered, row, palette), use_container_width=True)
        with b:
            top_gap_role = max({'CFO': row['cfo_need_score'] - filtered['cfo_need_score'].mean(), 'CTO': row['cto_need_score'] - filtered['cto_need_score'].mean(), 'CHRO': row['chro_need_score'] - filtered['chro_need_score'].mean(), 'CMO': row['cmo_need_score'] - filtered['cmo_need_score'].mean(), 'COO': row['coo_need_score'] - filtered['coo_need_score'].mean()}, key=lambda k: {'CFO': row['cfo_need_score'] - filtered['cfo_need_score'].mean(), 'CTO': row['cto_need_score'] - filtered['cto_need_score'].mean(), 'CHRO': row['chro_need_score'] - filtered['chro_need_score'].mean(), 'CMO': row['cmo_need_score'] - filtered['cmo_need_score'].mean(), 'COO': row['coo_need_score'] - filtered['coo_need_score'].mean()}[k])
            insight_card('What is driving the recommendation', f"The strongest positive gap versus the filtered portfolio norm is in {top_gap_role}. That is the clearest reason the recommendation prioritizes the current primary CXO route.")
            insight_card('How to use this in conversation', 'Use the positive bars as proof points for urgency and the negative bars to show why you are not leading with other executive roles first.')
    with lens3:
        a, b = st.columns([0.6, 0.4], gap='large')
        with a:
            st.altair_chart(prescriptive_action_chart(row, palette), use_container_width=True)
        with b:
            insight_card('What to do first', f"Start with {row['primary_fractional_cxo']} because it has the strongest need signal. Then use the close horizon and win probability to decide whether to move directly to proposal, pilot, or diagnostic scoping.")
            insight_card('What to do after the first win', f"The next expansion path is {row['secondary_fractional_cxo']} plus AI-supported roles. That gives you a logical upsell path without requiring the buyer to commit to a full executive bench immediately.")

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
