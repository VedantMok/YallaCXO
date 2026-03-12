import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO", page_icon="🚀", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def enable_altair_theme():
    def theme():
        return {
            "config": {
                "background": "transparent",
                "view": {"stroke": None},
                "title": {
                    "color": "#E8FFF3",
                    "fontSize": 18,
                    "font": "Space Grotesk",
                    "anchor": "start",
                    "fontWeight": 700,
                },
                "axis": {
                    "labelColor": "#B8D8C6",
                    "titleColor": "#DDFBEA",
                    "gridColor": "rgba(120, 170, 145, 0.18)",
                    "domainColor": "rgba(120, 170, 145, 0.28)",
                    "tickColor": "rgba(120, 170, 145, 0.28)",
                    "labelFont": "Inter",
                    "titleFont": "Inter",
                },
                "legend": {
                    "labelColor": "#CFEBDC",
                    "titleColor": "#E8FFF3",
                    "labelFont": "Inter",
                    "titleFont": "Inter",
                },
                "range": {
                    "category": ["#00F5A0", "#00D9F5", "#7C5CFF", "#FF7BEA", "#FFC857", "#29E7CD"]
                },
            }
        }

    try:
        alt.themes.register("yalla_futuristic", theme)
    except Exception:
        pass
    alt.themes.enable("yalla_futuristic")


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
        html, body, [class*="css"]  {font-family: 'Inter', sans-serif;}
        .stApp {
            background:
                radial-gradient(circle at 10% 20%, rgba(0, 245, 160, 0.08), transparent 28%),
                radial-gradient(circle at 90% 10%, rgba(0, 217, 245, 0.10), transparent 25%),
                linear-gradient(180deg, #07120D 0%, #091B14 34%, #0C1612 100%);
            color: #ECFFF4;
        }
        .block-container {padding-top: 1.1rem; padding-bottom: 2rem;}
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(8,19,14,0.98), rgba(9,27,20,0.96));
            border-right: 1px solid rgba(123, 163, 140, 0.18);
        }
        .hero-shell {
            background: linear-gradient(135deg, rgba(11,35,23,0.92) 0%, rgba(10,59,39,0.92) 42%, rgba(0,177,79,0.88) 100%);
            border: 1px solid rgba(110, 220, 165, 0.24);
            border-radius: 28px;
            padding: 1.3rem 1.45rem 1.15rem 1.45rem;
            box-shadow: 0 20px 54px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255,255,255,0.05);
            margin-bottom: 1rem;
            overflow: hidden;
            position: relative;
        }
        .hero-shell:before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transform: translateX(-100%);
            animation: shimmer 7s infinite linear;
        }
        @keyframes shimmer {100% {transform: translateX(100%);}}
        .hero-title {font-family: 'Space Grotesk', sans-serif; font-size: 2.25rem; font-weight: 700; margin: 0; color: #F4FFF9;}
        .hero-sub {margin-top: .38rem; color: #D7FCE7; max-width: 900px; line-height: 1.55;}
        .glass-card {
            background: linear-gradient(180deg, rgba(13,27,20,0.80), rgba(9,19,15,0.72));
            border: 1px solid rgba(124, 169, 144, 0.18);
            border-radius: 22px;
            padding: 1rem 1.05rem;
            box-shadow: 0 16px 36px rgba(0,0,0,0.18);
            backdrop-filter: blur(12px);
            transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
        }
        .glass-card:hover {transform: translateY(-2px); border-color: rgba(0,245,160,0.35); box-shadow: 0 18px 40px rgba(0,0,0,0.22);}
        .kpi-card {
            background: linear-gradient(180deg, rgba(11,25,19,0.84), rgba(8,17,13,0.80));
            border: 1px solid rgba(125, 167, 144, 0.17);
            border-radius: 20px;
            padding: .95rem 1rem;
            min-height: 108px;
            box-shadow: 0 14px 30px rgba(0,0,0,0.18);
        }
        .kpi-label {font-size: .74rem; text-transform: uppercase; letter-spacing: .08em; color: #95C4AB; margin-bottom: .3rem;}
        .kpi-value {font-family: 'Space Grotesk', sans-serif; font-size: 1.55rem; font-weight: 700; color: #F0FFF6; margin-bottom: .2rem;}
        .kpi-sub {font-size: .84rem; color: #B8D8C6; line-height: 1.35;}
        .badge-row {display:flex; gap:.55rem; flex-wrap:wrap; margin-top:.8rem;}
        .badge-pill {
            display:inline-flex; align-items:center; gap:.4rem; padding:.45rem .72rem;
            background: rgba(255,255,255,0.08); color:#E9FFF4; border:1px solid rgba(190,255,223,0.12);
            border-radius:999px; font-size:.82rem;
        }
        .section-kicker {font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; color: #8FD5B0; margin-bottom: .28rem;}
        .section-title {font-family: 'Space Grotesk', sans-serif; color: #ECFFF4; font-size: 1.35rem; margin: .1rem 0 .15rem 0;}
        .section-copy {color:#AFCFBE; line-height:1.52; margin-bottom:.9rem;}
        .insight-box {
            background: linear-gradient(180deg, rgba(10,22,16,0.84), rgba(8,17,13,0.76));
            border:1px solid rgba(124,167,144,0.18);
            border-left:4px solid #00F5A0;
            border-radius:18px;
            padding:.95rem 1rem;
            box-shadow:0 12px 28px rgba(0,0,0,0.16);
            height:100%;
        }
        .insight-box h4 {margin:0 0 .4rem 0; color:#F1FFF8; font-size:1rem;}
        .insight-box p {margin:0; color:#B9D8C8; line-height:1.52;}
        .callout-box {
            background: linear-gradient(180deg, rgba(10,33,22,0.92), rgba(11,54,34,0.82));
            border:1px solid rgba(0,245,160,0.18);
            border-radius:22px; padding:1rem 1.05rem; margin:.65rem 0 1rem 0;
            box-shadow:0 16px 32px rgba(0,0,0,0.18);
        }
        .callout-box strong {color:#F2FFF8;}
        .mini-stat-grid {display:grid; grid-template-columns:repeat(3, 1fr); gap:.8rem; margin-top:.9rem;}
        .mini-stat {background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07); border-radius:18px; padding:.85rem .95rem;}
        .mini-stat .label {color:#8FC9AD; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em;}
        .mini-stat .value {font-family:'Space Grotesk',sans-serif; color:#F2FFF8; font-size:1.15rem; margin-top:.22rem;}
        .mini-stat .sub {color:#B6D4C4; font-size:.82rem; margin-top:.18rem; line-height:1.4;}
        .dataframe, div[data-testid="stDataFrame"] {border-radius:18px; overflow:hidden;}
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {background: rgba(255,255,255,0.04); border-color: rgba(130,170,150,0.18);}
        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(11,25,19,0.84), rgba(8,17,13,0.78));
            border: 1px solid rgba(125,167,144,0.17);
            border-radius: 20px;
            padding: .62rem .75rem;
            box-shadow: 0 12px 28px rgba(0,0,0,0.16);
        }
        .stTabs [data-baseweb="tab-list"] {gap: .5rem;}
        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.04); border:1px solid rgba(130,170,150,0.12); border-radius:14px; color:#B8D8C6; padding:.55rem .95rem;
        }
        .stTabs [aria-selected="true"] {background: linear-gradient(180deg, rgba(0,245,160,0.14), rgba(0,217,245,0.14)); color:#F1FFF8; border-color: rgba(0,245,160,0.32);}
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


def section_header(kicker, title, copy):
    st.markdown(
        f"<div class='section-kicker'>{kicker}</div><div class='section-title'>{title}</div><div class='section-copy'>{copy}</div>",
        unsafe_allow_html=True,
    )


def insight_card(title, text):
    st.markdown(f"<div class='insight-box'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def kpi_card(title, value, subtitle):
    st.markdown(
        f"<div class='kpi-card'><div class='kpi-label'>{title}</div><div class='kpi-value'>{value}</div><div class='kpi-sub'>{subtitle}</div></div>",
        unsafe_allow_html=True,
    )


def callout(text):
    st.markdown(f"<div class='callout-box'>{text}</div>", unsafe_allow_html=True)


def role_profile_chart(row):
    df = pd.DataFrame({
        'Role': ['CFO', 'CTO', 'CHRO', 'CMO', 'COO'],
        'Need Score': [row['cfo_need_score'], row['cto_need_score'], row['chro_need_score'], row['cmo_need_score'], row['coo_need_score']]
    }).sort_values('Need Score', ascending=True)

    bars = alt.Chart(df).mark_bar(cornerRadiusEnd=10, height=26).encode(
        x=alt.X('Need Score:Q', title='Need Score', scale=alt.Scale(domain=[0, 100])),
        y=alt.Y('Role:N', sort=None, title=''),
        color=alt.Color('Role:N', title=''),
        tooltip=['Role', 'Need Score']
    )
    text = alt.Chart(df).mark_text(align='left', dx=8, color='#E8FFF3', font='Inter', fontSize=12).encode(
        x='Need Score:Q', y=alt.Y('Role:N', sort=None), text=alt.Text('Need Score:Q', format='.1f')
    )
    return (bars + text).properties(title='Role fit and recommendation strength', height=300)


def company_cost_chart(row):
    df = pd.DataFrame({
        'Model': ['Full-time executive stack', 'Yalla CXO hybrid model', 'Annual savings unlocked'],
        'Value': [row['full_time_equivalent_cost_aed'], row['fractional_ai_solution_cost_aed'], row['estimated_annual_savings_aed']],
        'Group': ['Cost', 'Cost', 'Savings']
    })
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, size=52).encode(
        x=alt.X('Model:N', title=''),
        y=alt.Y('Value:Q', title='Annual AED Value'),
        color=alt.Color('Group:N', scale=alt.Scale(domain=['Cost', 'Savings'], range=['#4D5D59', '#00F5A0']), title=''),
        tooltip=['Model', alt.Tooltip('Value:Q', format=',.0f')]
    )
    text = alt.Chart(df).mark_text(dy=-10, color='#E8FFF3', font='Inter', fontSize=11).encode(
        x='Model:N', y='Value:Q', text=alt.Text('Value:Q', format=',.0f')
    )
    return (bars + text).properties(title='Economic case versus full-time hiring', height=320)


def operating_signal_chart(row):
    signals = pd.DataFrame({
        'Signal': ['Cash volatility', 'Digital maturity', 'Process efficiency', 'Attrition', 'Campaign ROI', 'Win probability'],
        'Value': [row['cash_flow_volatility_score'], row['digital_maturity_score'], row['process_efficiency_score'], row['attrition_rate_pct'] * 3, row['campaign_roi_x'] * 20, row['win_probability'] * 100],
        'Category': ['Finance', 'Technology', 'Operations', 'People', 'Growth', 'Commercial']
    }).sort_values('Value', ascending=True)
    bars = alt.Chart(signals).mark_bar(cornerRadiusEnd=10, height=22).encode(
        x=alt.X('Value:Q', title='Scaled score / intensity'),
        y=alt.Y('Signal:N', sort=None, title=''),
        color=alt.Color('Category:N', title=''),
        tooltip=['Signal', 'Category', alt.Tooltip('Value:Q', format='.1f')]
    )
    return bars.properties(title='Operating signal snapshot', height=300)


def peer_position_chart(filtered, row):
    peers = filtered.copy()
    peers['selected'] = peers['company_name'].eq(row['company_name'])
    x_mid = peers['estimated_annual_savings_aed'].median()
    y_mid = peers['expected_annual_contract_value_aed'].median()

    rules_x = alt.Chart(pd.DataFrame({'x': [x_mid]})).mark_rule(strokeDash=[6, 6], color='rgba(210,255,230,0.25)').encode(x='x:Q')
    rules_y = alt.Chart(pd.DataFrame({'y': [y_mid]})).mark_rule(strokeDash=[6, 6], color='rgba(210,255,230,0.25)').encode(y='y:Q')

    base = alt.Chart(peers).mark_circle(opacity=0.76, stroke='white', strokeWidth=0.6).encode(
        x=alt.X('estimated_annual_savings_aed:Q', title='Estimated Annual Savings (AED)'),
        y=alt.Y('expected_annual_contract_value_aed:Q', title='Expected ACV (AED)'),
        size=alt.Size('win_probability:Q', title='Win Probability', scale=alt.Scale(range=[70, 900])),
        color=alt.condition(alt.datum.selected, alt.value('#FF5D8F'), alt.Color('primary_fractional_cxo:N', title='Primary CXO')),
        tooltip=['company_name', 'sector', 'primary_fractional_cxo', 'secondary_fractional_cxo', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability']
    )
    label = alt.Chart(peers[peers['selected']]).mark_text(dx=8, dy=-8, color='#F4FFF9', font='Inter', fontSize=11).encode(
        x='estimated_annual_savings_aed:Q', y='expected_annual_contract_value_aed:Q', text='company_name:N'
    )
    return (rules_x + rules_y + base + label).properties(title='Portfolio position of the selected company', height=360)


def savings_trajectory_chart(row):
    months = list(range(1, 13))
    full_monthly = row['full_time_equivalent_cost_aed'] / 12
    yalla_monthly = row['fractional_ai_solution_cost_aed'] / 12
    data = pd.DataFrame({
        'Month': months,
        'Full-time cumulative cost': [full_monthly * m for m in months],
        'Yalla CXO cumulative cost': [yalla_monthly * m for m in months],
    })
    long = data.melt('Month', var_name='Path', value_name='Value')
    line = alt.Chart(long).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('Month:O', title='Month'),
        y=alt.Y('Value:Q', title='Cumulative AED Cost'),
        color=alt.Color('Path:N', scale=alt.Scale(domain=['Full-time cumulative cost', 'Yalla CXO cumulative cost'], range=['#FF7B72', '#00F5A0']), title=''),
        tooltip=['Month', 'Path', alt.Tooltip('Value:Q', format=',.0f')]
    )
    return line.properties(title='12-month cost path comparison', height=320)


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
        'company_name': 'Comparable company',
        'sector': 'Sector',
        'primary_fractional_cxo': 'Primary CXO',
        'estimated_annual_savings_aed': 'Savings',
        'expected_annual_contract_value_aed': 'Expected ACV',
        'win_probability': 'Win Prob.'
    })


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
    badges = f"""
    <div class='badge-row'>
        <div class='badge-pill'>Sector · {row['sector']}</div>
        <div class='badge-pill'>Revenue band · {row['revenue_band']}</div>
        <div class='badge-pill'>Account tier · {row['account_tier']}</div>
        <div class='badge-pill'>Urgency · {row['urgency_tier']} ({row['urgency_score']:.1f})</div>
        <div class='badge-pill'>Service mix · {row['service_mix']}</div>
    </div>
    """
    st.markdown(
        f"""
        <div class='glass-card'>
            <div class='section-kicker'>Selected company</div>
            <div class='section-title'>{row['company_name']}</div>
            <div class='section-copy'>This view is designed to help you pitch one company at a time by showing its executive need profile, cost advantage, portfolio position, and expansion path in a single narrative flow.</div>
            {badges}
            <div class='mini-stat-grid'>
                <div class='mini-stat'><div class='label'>Primary CXO</div><div class='value'>{row['primary_fractional_cxo']}</div><div class='sub'>Lead recommendation for first engagement.</div></div>
                <div class='mini-stat'><div class='label'>Secondary CXO</div><div class='value'>{row['secondary_fractional_cxo']}</div><div class='sub'>Best expansion role after the first intervention.</div></div>
                <div class='mini-stat'><div class='label'>Expected LTV</div><div class='value'>{fmt_aed(row['expected_account_ltv_aed'])}</div><div class='sub'>Longer-term account value if the relationship expands well.</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


df = load_data()
enable_altair_theme()
inject_css()

st.markdown(
    """
    <div class='hero-shell'>
        <div class='hero-title'>Yalla CXO</div>
        <div class='hero-sub'>Futuristic, company-first pitching dashboard for showing exactly why a given corporate should buy a fractional CXO solution, how much it can save versus full-time hiring, and where AI-supported expansion creates additional value.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header('Portfolio filters')
    sectors = st.multiselect('Sector', sorted(df['sector'].unique()), default=sorted(df['sector'].unique()))
    roles = st.multiselect('Primary CXO', sorted(df['primary_fractional_cxo'].unique()), default=sorted(df['primary_fractional_cxo'].unique()))
    urgency = st.multiselect('Urgency Tier', sorted(df['urgency_tier'].unique()), default=sorted(df['urgency_tier'].unique()))
    tiers = st.multiselect('Account Tier', sorted(df['account_tier'].unique()), default=sorted(df['account_tier'].unique()))
    revenue_range = st.slider('Revenue (AED bn)', float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max()), (float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max())))
    min_win = st.slider('Minimum win probability', 0.0, 1.0, 0.0, 0.01)

filtered = df[
    df['sector'].isin(sectors)
    & df['primary_fractional_cxo'].isin(roles)
    & df['urgency_tier'].isin(urgency)
    & df['account_tier'].isin(tiers)
    & df['revenue_aed_bn'].between(revenue_range[0], revenue_range[1])
    & (df['win_probability'] >= min_win)
].copy()

if filtered.empty:
    st.warning('No companies match the current filters.')
    st.stop()

selected_company = st.selectbox('Choose a company to pitch', filtered.sort_values('company_name')['company_name'].tolist())
row = filtered.loc[filtered['company_name'] == selected_company].iloc[0]
texts = recommendation_text(row, filtered)

profile_shell(row)

c1, c2, c3, c4, c5 = st.columns(5)
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

tab1, tab2, tab3 = st.tabs(['Recommendation', 'Economics', 'Portfolio Context'])

with tab1:
    section_header('Diagnostic', 'Lead with the right executive problem', 'The goal of this section is to make the recommendation feel evidence-based. It shows which executive need dominates, what operational signals support that conclusion, and what talking points should lead the meeting.')
    a, b = st.columns([0.55, 0.45])
    with a:
        st.altair_chart(role_profile_chart(row), use_container_width=True)
    with b:
        st.altair_chart(operating_signal_chart(row), use_container_width=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        insight_card('Primary recommendation', texts['lead'])
    with i2:
        insight_card('Why now', texts['timing'])
    with i3:
        insight_card('Expansion logic', texts['upsell'])

with tab2:
    section_header('Economics', 'Make the savings case impossible to miss', 'This section is built to help you sell the financial logic in one glance: compare full-time executive cost versus the Yalla CXO hybrid model, then show how that savings path evolves over a 12-month horizon.')
    a, b = st.columns(2)
    with a:
        st.altair_chart(company_cost_chart(row), use_container_width=True)
    with b:
        st.altair_chart(savings_trajectory_chart(row), use_container_width=True)
    i1, i2 = st.columns(2)
    with i1:
        insight_card('Economic justification', texts['economics'])
    with i2:
        insight_card('Role benchmark', texts['benchmark'])

with tab3:
    section_header('Positioning', 'Show where this company sits inside the broader opportunity map', 'This section helps you explain whether the selected company is a standout savings case, a standout revenue case, or a balanced priority. It also gives you a shortlist of comparable accounts for pattern-based storytelling.')
    a, b = st.columns([0.58, 0.42])
    with a:
        st.altair_chart(peer_position_chart(filtered, row), use_container_width=True)
    with b:
        insight_card('Sector proof point', texts['sector'])
        insight_card('Meeting talk track', f"Open with the {row['primary_fractional_cxo']}-led pain, quantify the {fmt_aed(row['estimated_annual_savings_aed'])} savings gap, then position {row['secondary_fractional_cxo']} and the AI-supported operating layer as the low-friction expansion path.")
    st.subheader('Closest comparable accounts')
    st.dataframe(comparable_accounts(filtered, row), use_container_width=True, hide_index=True)

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
