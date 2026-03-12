import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def inject_css():
    st.markdown("""
    <style>
    .main {background: linear-gradient(180deg, #F7FCF9 0%, #FFFFFF 32%);}    
    .hero {background: linear-gradient(135deg, #083A21 0%, #0B6B3A 50%, #00B14F 100%); padding: 1.3rem 1.45rem; border-radius: 24px; color: white; box-shadow: 0 16px 36px rgba(0,177,79,.18); margin-bottom: 1rem;}
    .hero h1 {margin:0; font-size:2.05rem;} .hero p {margin:.38rem 0 0 0; opacity:.96; line-height:1.5;}
    .callout {background:#F3FBF6; border:1px solid #DCEEE3; border-radius:18px; padding:1rem 1.05rem; margin:.4rem 0 .9rem 0;} .callout strong {color:#0B6B3A;}
    .insight-box {background:#FFFFFF; border:1px solid #E2EFE8; border-left:5px solid #00B14F; border-radius:18px; padding:1rem 1rem .95rem 1rem; box-shadow:0 8px 18px rgba(0,0,0,.03); height:100%;}
    .insight-box h4 {margin:.02rem 0 .4rem 0; color:#143524;} .insight-box p {margin:0; color:#4B6658; line-height:1.55;}
    .decision-strip {display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin:.7rem 0 1rem 0;}
    .decision-card {background:#FFFFFF; border:1px solid #E2EFE8; border-radius:18px; padding:1rem; box-shadow:0 8px 18px rgba(0,0,0,.03);} 
    .decision-card h5 {margin:0 0 .35rem 0; color:#607A6A; text-transform:uppercase; letter-spacing:.05em; font-size:.72rem;} 
    .decision-card h3 {margin:0 0 .35rem 0; color:#143524; font-size:1.18rem;} 
    .decision-card p {margin:0; color:#4B6658; line-height:1.45; font-size:.92rem;}
    .section-title {margin-top:.35rem; color:#143524;}
    div[data-testid="stMetric"] {background:#FFFFFF; border:1px solid #E2EFE8; border-radius:18px; padding:.55rem .65rem; box-shadow:0 8px 18px rgba(0,0,0,.03);}
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


def insight_card(title, text):
    st.markdown(f"<div class='insight-box'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def role_profile_chart(row):
    df = pd.DataFrame({
        'Role':['CFO','CTO','CHRO','CMO','COO'],
        'Need Score':[row['cfo_need_score'], row['cto_need_score'], row['chro_need_score'], row['cmo_need_score'], row['coo_need_score']]
    }).sort_values('Need Score', ascending=False)
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('Role:N', title='CXO Role'),
        y=alt.Y('Need Score:Q', title='Need Score'),
        color=alt.Color('Role:N', title=''),
        tooltip=['Role','Need Score']
    ).properties(title='Why this company gets this recommendation', height=320)


def company_cost_chart(row):
    df = pd.DataFrame({
        'Cost Type':['Full-time equivalent','Yalla CXO model','Annual savings'],
        'Value':[row['full_time_equivalent_cost_aed'], row['fractional_ai_solution_cost_aed'], row['estimated_annual_savings_aed']],
        'Group':['Cost','Cost','Savings']
    })
    return alt.Chart(df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('Cost Type:N', title=''),
        y=alt.Y('Value:Q', title='AED Value'),
        color=alt.Color('Group:N', scale=alt.Scale(domain=['Cost','Savings'], range=['#94A3B8','#00B14F']), title=''),
        tooltip=['Cost Type', alt.Tooltip('Value:Q', format=',.0f')]
    ).properties(title='Company-level cost comparison', height=320)


def metric_snapshot_chart(row):
    metrics = pd.DataFrame({
        'Metric':['Revenue (AED bn)','Revenue growth %','Employee count','Digital maturity','Cash flow volatility','Process efficiency','Attrition %','Expected ROI x'],
        'Value':[row['revenue_aed_bn'], row['revenue_growth_12m_pct'], row['employee_count'], row['digital_maturity_score'], row['cash_flow_volatility_score'], row['process_efficiency_score'], row['attrition_rate_pct'], row['expected_roi_multiple']]
    })
    return alt.Chart(metrics).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8).encode(
        x=alt.X('Value:Q', title='Value'),
        y=alt.Y('Metric:N', sort='-x', title=''),
        tooltip=['Metric','Value']
    ).properties(title='Company operating snapshot', height=340)


def peer_position_chart(filtered, row):
    peers = filtered.copy()
    peers['selected'] = peers['company_name'].eq(row['company_name'])
    base = alt.Chart(peers).mark_circle(opacity=0.75, stroke='white', strokeWidth=0.6).encode(
        x=alt.X('estimated_annual_savings_aed:Q', title='Estimated Annual Savings (AED)'),
        y=alt.Y('expected_annual_contract_value_aed:Q', title='Expected Annual Contract Value (AED)'),
        size=alt.Size('win_probability:Q', title='Win Probability', scale=alt.Scale(range=[80, 900])),
        color=alt.condition(alt.datum.selected, alt.value('#D62828'), alt.Color('primary_fractional_cxo:N', title='Primary CXO')),
        tooltip=['company_name','sector','primary_fractional_cxo','secondary_fractional_cxo','estimated_annual_savings_aed','expected_annual_contract_value_aed','win_probability']
    )
    label_df = peers[peers['selected']]
    labels = alt.Chart(label_df).mark_text(dx=8, dy=-8, fontSize=11, color='#143524').encode(
        x='estimated_annual_savings_aed:Q', y='expected_annual_contract_value_aed:Q', text='company_name:N'
    )
    return (base + labels).properties(title='How this company compares with the filtered portfolio', height=360)


def recommendation_text(row, filtered):
    sector_rank = filtered.groupby('sector')['weighted_pipeline_value_aed'].sum().rank(ascending=False, method='dense')
    sector_position = int(sector_rank[row['sector']]) if row['sector'] in sector_rank.index else None
    return {
        'lead': f"Lead with a {row['primary_fractional_cxo']}-first offer. This is the strongest modeled pain point for {row['company_name']}, while {row['secondary_fractional_cxo']} should be positioned as the natural expansion path once the first engagement proves value.",
        'economics': f"The clearest buying argument is cost efficiency: the modeled executive bench would cost {fmt_aed(row['full_time_equivalent_cost_aed'])} under a full-time structure, versus {fmt_aed(row['fractional_ai_solution_cost_aed'])} through Yalla CXO, unlocking {fmt_aed(row['estimated_annual_savings_aed'])} in annual savings.",
        'timing': f"This account carries a {row['win_probability']*100:.1f}% modeled win probability and an expected close time of {int(row['expected_close_days'])} days, which means it should be treated as a live commercial opportunity rather than a long-horizon prospect.",
        'sector': f"{row['sector']} ranks #{sector_position} in weighted pipeline contribution within the current filter set, so this company can also serve as a sector-specific proof point in your broader Dubai go-to-market story.",
        'upsell': f"After the primary engagement, the best expansion path is {row['secondary_fractional_cxo']} plus AI-supported roles: {row['ai_supported_roles']}. The expected next-service expansion window is {int(row['next_service_expansion_days'])} days."
    }


def top_comparables(filtered, row):
    subset = filtered.copy()
    subset['distance'] = (
        (subset['revenue_aed_bn'] - row['revenue_aed_bn']).abs() * 2
        + (subset['urgency_score'] - row['urgency_score']).abs() * 0.4
        + (subset['expected_annual_contract_value_aed'] - row['expected_annual_contract_value_aed']).abs() / 500000
    )
    subset = subset[subset['company_name'] != row['company_name']].sort_values('distance').head(5)
    out = subset[['company_name','sector','primary_fractional_cxo','estimated_annual_savings_aed','expected_annual_contract_value_aed','win_probability']].copy()
    out['estimated_annual_savings_aed'] = out['estimated_annual_savings_aed'].map(fmt_aed)
    out['expected_annual_contract_value_aed'] = out['expected_annual_contract_value_aed'].map(fmt_aed)
    out['win_probability'] = (out['win_probability']*100).round(1).astype(str) + '%'
    return out.rename(columns={
        'company_name':'Comparable company','sector':'Sector','primary_fractional_cxo':'Primary CXO','estimated_annual_savings_aed':'Savings',
        'expected_annual_contract_value_aed':'Expected ACV','win_probability':'Win Prob.'
    })


def portfolio_recommendation_cards(row, filtered):
    same_role = filtered[filtered['primary_fractional_cxo'] == row['primary_fractional_cxo']]
    role_avg_save = same_role['estimated_annual_savings_aed'].mean()
    role_avg_win = same_role['win_probability'].mean()
    same_sector = filtered[filtered['sector'] == row['sector']]
    sector_pipe = same_sector['weighted_pipeline_value_aed'].sum()
    html = f"""
    <div class='decision-strip'>
        <div class='decision-card'>
            <h5>Primary pitch</h5>
            <h3>{row['primary_fractional_cxo']}-led entry</h3>
            <p>Use this role as the lead offer for {row['company_name']} because it has the highest modeled need score and creates the clearest justification for intervention.</p>
        </div>
        <div class='decision-card'>
            <h5>Economic proof</h5>
            <h3>{fmt_aed(row['estimated_annual_savings_aed'])} saved</h3>
            <p>This company shows a {row['estimated_savings_pct']:.1f}% modeled savings gap versus full-time executive hiring, which is the strongest commercial anchor for the conversation.</p>
        </div>
        <div class='decision-card'>
            <h5>Expansion path</h5>
            <h3>{row['secondary_fractional_cxo']} + AI add-ons</h3>
            <p>After the first engagement, move into the secondary role and the AI-supported operating layer to expand contract value without needing a full additional executive bench.</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    return role_avg_save, role_avg_win, sector_pipe


df = load_data()
inject_css()

st.markdown("""
<div class='hero'>
    <h1>Yalla CXO</h1>
    <p>Company-first executive dashboard for pitching one corporate at a time: diagnose the need, quantify the savings versus full-time hiring, recommend the right fractional CXO, and show the expansion path through secondary roles and AI-supported delivery.</p>
</div>
""", unsafe_allow_html=True)

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

company = st.selectbox('Choose a company to pitch', filtered.sort_values('company_name')['company_name'].tolist())
row = filtered.loc[filtered['company_name'] == company].iloc[0]
texts = recommendation_text(row, filtered)
role_avg_save, role_avg_win, sector_pipe = portfolio_recommendation_cards(row, filtered)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric('Primary CXO', row['primary_fractional_cxo'])
k2.metric('Secondary CXO', row['secondary_fractional_cxo'])
k3.metric('Annual savings', fmt_aed(row['estimated_annual_savings_aed']))
k4.metric('Expected ACV', fmt_aed(row['expected_annual_contract_value_aed']))
k5.metric('Win probability', f"{row['win_probability']*100:.1f}%")

st.markdown(f"<div class='callout'><strong>Recommendation for {row['company_name']}:</strong> {texts['lead']} {texts['economics']}</div>", unsafe_allow_html=True)

st.markdown("<h3 class='section-title'>1. Company profile and commercial recommendation</h3>", unsafe_allow_html=True)
c1, c2 = st.columns([0.56, 0.44])
with c1:
    st.markdown(f"""
    ### {row['company_name']}
    **Sector:** {row['sector']}  
    **Revenue band:** {row['revenue_band']}  
    **Account tier:** {row['account_tier']}  
    **Urgency:** {row['urgency_tier']} ({row['urgency_score']:.1f})  
    **Service mix:** {row['service_mix']}  
    **Expected LTV:** {fmt_aed(row['expected_account_ltv_aed'])}  
    **Ideal next action:** {row['ideal_next_action']}  
    **AI-supported roles:** {row['ai_supported_roles']}  
    **AI add-ons:** {row['ai_agent_addons']}
    """)
    insight_card('Why this recommendation fits', texts['lead'])
    insight_card('Why the buyer should care now', texts['timing'])
with c2:
    st.altair_chart(role_profile_chart(row), use_container_width=True)
    st.caption('This chart shows which executive pain is strongest for the selected company, so you can justify why the recommended primary role should lead the conversation.')

st.markdown("<h3 class='section-title'>2. Economic case versus full-time hiring</h3>", unsafe_allow_html=True)
c3, c4 = st.columns([0.5, 0.5])
with c3:
    st.altair_chart(company_cost_chart(row), use_container_width=True)
    st.caption('Use this chart in the pitch to make the savings argument visible in one glance: full-time executive cost base versus the Yalla CXO model and the savings gap created between them.')
with c4:
    st.altair_chart(metric_snapshot_chart(row), use_container_width=True)
    st.caption('These metrics explain the business context behind the recommendation, so the solution appears diagnostic and specific rather than generic.')

i1, i2 = st.columns(2)
with i1:
    insight_card('Economic justification', texts['economics'])
with i2:
    insight_card('Commercial benchmark', f"Across companies with a primary {row['primary_fractional_cxo']} recommendation in the current filtered set, the average modeled savings is {fmt_aed(role_avg_save)} and the average win probability is {role_avg_win*100:.1f}%.")

st.markdown("<h3 class='section-title'>3. Portfolio context: where this company sits</h3>", unsafe_allow_html=True)
c5, c6 = st.columns([0.58, 0.42])
with c5:
    st.altair_chart(peer_position_chart(filtered, row), use_container_width=True)
    st.caption(f"The selected company is highlighted in red. This shows whether it is a strong savings story, a strong revenue story, or both relative to the rest of the filtered portfolio.")
with c6:
    insight_card('Sector positioning', texts['sector'])
    insight_card('Expansion path', texts['upsell'])
    insight_card('Sector-level sales relevance', f"The selected company sits inside a sector contributing {fmt_aed(sector_pipe)} in weighted pipeline value within the current portfolio filter, which means it can also be used as a sector proof point during broader business development.")

st.markdown("<h3 class='section-title'>4. Suggested pitch support</h3>", unsafe_allow_html=True)
c7, c8 = st.columns([0.54, 0.46])
with c7:
    st.subheader('Closest comparable accounts')
    st.dataframe(top_comparables(filtered, row), use_container_width=True, hide_index=True)
with c8:
    insight_card('Suggested talk track', f"Start with the {row['primary_fractional_cxo']}-led need, quantify the savings delta of {fmt_aed(row['estimated_annual_savings_aed'])}, then explain how {row['secondary_fractional_cxo']} and AI-supported roles create a broader executive operating model without full-time hiring overhead.")
    insight_card('What to ask in the meeting', f"Confirm whether the company is currently feeling the pain captured in the top two role scores. If yes, use that to move from a diagnostic conversation into a scoped proposal and pilot discussion around {row['ideal_next_action'].lower()}.")

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
