import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def inject_css():
    st.markdown("""
    <style>
    .main {background: linear-gradient(180deg, #F7FCF9 0%, #FFFFFF 30%);}    
    .hero {background: linear-gradient(135deg, #083A21 0%, #0B6B3A 45%, #00B14F 100%); padding: 1.35rem 1.45rem; border-radius: 24px; color: white; box-shadow: 0 16px 36px rgba(0,177,79,.18); margin-bottom: 1rem;}
    .hero h1 {margin:0; font-size:2.1rem;}
    .hero p {margin:.38rem 0 0 0; opacity:.96; line-height:1.5;}
    .callout {background:#F3FBF6; border:1px solid #DCEEE3; border-radius:18px; padding:1rem 1.05rem; margin:.4rem 0 .9rem 0;}
    .callout strong {color:#0B6B3A;}
    .insight-box {background:#FFFFFF; border:1px solid #E2EFE8; border-left:5px solid #00B14F; border-radius:18px; padding:1rem 1rem .95rem 1rem; box-shadow:0 8px 18px rgba(0,0,0,.03); height:100%;}
    .insight-box h4 {margin:.02rem 0 .4rem 0; color:#143524;}
    .insight-box p {margin:0; color:#4B6658; line-height:1.55;}
    .section-title {margin-top:.3rem; color:#143524;}
    .decision-strip {display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin:.7rem 0 1rem 0;}
    .decision-card {background:#FFFFFF; border:1px solid #E2EFE8; border-radius:18px; padding:1rem; box-shadow:0 8px 18px rgba(0,0,0,.03);}
    .decision-card h5 {margin:0 0 .35rem 0; color:#607A6A; text-transform:uppercase; letter-spacing:.05em; font-size:.72rem;}
    .decision-card h3 {margin:0 0 .35rem 0; color:#143524; font-size:1.2rem;}
    .decision-card p {margin:0; color:#4B6658; line-height:1.45; font-size:.92rem;}
    .subtle {color:#607A6A; font-size:.92rem;}
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


def build_summary(filtered):
    top_sector = filtered.groupby('sector', as_index=False).agg(weighted_pipeline=('weighted_pipeline_value_aed','sum')).sort_values('weighted_pipeline', ascending=False).iloc[0]
    top_role = filtered['primary_fractional_cxo'].value_counts().idxmax()
    top_account = filtered.sort_values('weighted_pipeline_value_aed', ascending=False).iloc[0]
    roi_leader = filtered.sort_values('expected_roi_multiple', ascending=False).iloc[0]
    return top_sector, top_role, top_account, roi_leader


def compare_cost_chart(filtered):
    full_time = filtered['full_time_equivalent_cost_aed'].sum()
    solution = filtered['fractional_ai_solution_cost_aed'].sum()
    savings = filtered['estimated_annual_savings_aed'].sum()
    chart_df = pd.DataFrame({
        'Cost Type': ['Full-time hiring model', 'Yalla CXO model', 'Annual savings unlocked'],
        'Value': [full_time, solution, savings],
        'Group': ['Cost', 'Cost', 'Savings']
    })
    return alt.Chart(chart_df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('Cost Type:N', title=''),
        y=alt.Y('Value:Q', title='Annual AED Value'),
        color=alt.Color('Group:N', scale=alt.Scale(domain=['Cost','Savings'], range=['#7F8C8D','#00B14F']), title=''),
        tooltip=['Cost Type', alt.Tooltip('Value:Q', format=',.0f')]
    ).properties(title='Cost comparison: full-time hiring vs Yalla CXO solution', height=360)


def savings_bridge_chart(filtered):
    full_time = filtered['full_time_equivalent_cost_aed'].sum()
    solution = filtered['fractional_ai_solution_cost_aed'].sum()
    savings = full_time - solution
    bridge = pd.DataFrame({
        'Step': ['Full-time cost base', 'Savings unlocked', 'Yalla CXO delivery cost'],
        'Value': [full_time, savings, solution],
        'Type': ['Base', 'Savings', 'Residual']
    })
    return alt.Chart(bridge).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X('Step:N', title=''),
        y=alt.Y('Value:Q', title='AED'),
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Base','Savings','Residual'], range=['#A0AEC0','#00B14F','#0B6B3A']), title=''),
        tooltip=['Step', alt.Tooltip('Value:Q', format=',.0f')]
    ).properties(title='Value bridge for the filtered opportunity set', height=360)


def sector_role_heatmap(filtered):
    role_cols = ['cfo_need_score','cto_need_score','chro_need_score','cmo_need_score','coo_need_score']
    role_names = ['CFO','CTO','CHRO','CMO','COO']
    h = filtered.groupby('sector')[role_cols].mean().reset_index()
    h.columns = ['sector'] + role_names
    melted = h.melt('sector', var_name='Role', value_name='Avg Need Score')
    base = alt.Chart(melted).encode(x='Role:N', y=alt.Y('sector:N', sort='-color'))
    heat = base.mark_rect().encode(
        color=alt.Color('Avg Need Score:Q', scale=alt.Scale(scheme='yellowgreenblue')),
        tooltip=['sector','Role', alt.Tooltip('Avg Need Score:Q', format='.1f')]
    )
    text = base.mark_text(size=11).encode(text=alt.Text('Avg Need Score:Q', format='.1f'))
    return (heat + text).properties(title='Where each CXO role is most needed', height=420)


def value_quadrant(filtered):
    top = filtered.nlargest(min(12, len(filtered)), 'weighted_pipeline_value_aed').copy()
    base = alt.Chart(filtered).mark_circle(opacity=0.78, stroke='white', strokeWidth=0.7).encode(
        x=alt.X('estimated_annual_savings_aed:Q', title='Estimated Annual Savings (AED)'),
        y=alt.Y('weighted_pipeline_value_aed:Q', title='Weighted Pipeline Value (AED)'),
        size=alt.Size('expected_account_ltv_aed:Q', title='Expected LTV', scale=alt.Scale(range=[70, 1000])),
        color=alt.Color('primary_fractional_cxo:N', title='Primary CXO'),
        tooltip=['company_name','sector','primary_fractional_cxo','secondary_fractional_cxo','estimated_annual_savings_aed','weighted_pipeline_value_aed','expected_account_ltv_aed','win_probability']
    )
    labels = alt.Chart(top).mark_text(align='left', dx=7, dy=-6, fontSize=10, color='#143524').encode(
        x='estimated_annual_savings_aed:Q', y='weighted_pipeline_value_aed:Q', text='company_name:N'
    )
    return (base + labels).properties(title='Which accounts are most sellable right now', height=420)


def projection_chart(filtered):
    proj = pd.DataFrame({
        'Horizon': ['Current annual opportunity', '2-quarter forecast', 'Expected account LTV'],
        'Value': [
            filtered['expected_annual_contract_value_aed'].sum(),
            filtered['forecast_2q_revenue_aed'].sum(),
            filtered['expected_account_ltv_aed'].sum()
        ],
        'Metric': ['ACV','Forecast','LTV']
    })
    return alt.Chart(proj).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x='Horizon:N',
        y=alt.Y('Value:Q', title='AED Value'),
        color=alt.Color('Metric:N', scale=alt.Scale(domain=['ACV','Forecast','LTV'], range=['#00B14F','#2F855A','#0B6B3A']), title=''),
        tooltip=['Horizon', alt.Tooltip('Value:Q', format=',.0f')]
    ).properties(title='Commercial projection from the filtered portfolio', height=360)


def top_accounts_table(filtered, n=12):
    cols = ['company_name','sector','primary_fractional_cxo','secondary_fractional_cxo','estimated_annual_savings_aed','expected_annual_contract_value_aed','expected_roi_multiple','ideal_next_action']
    t = filtered.sort_values(['weighted_pipeline_value_aed','win_probability'], ascending=False)[cols].head(n).copy()
    t['estimated_annual_savings_aed'] = t['estimated_annual_savings_aed'].map(fmt_aed)
    t['expected_annual_contract_value_aed'] = t['expected_annual_contract_value_aed'].map(fmt_aed)
    t['expected_roi_multiple'] = t['expected_roi_multiple'].round(2).astype(str) + 'x'
    return t.rename(columns={
        'company_name':'Company','sector':'Sector','primary_fractional_cxo':'Primary CXO','secondary_fractional_cxo':'Secondary CXO',
        'estimated_annual_savings_aed':'Annual Savings','expected_annual_contract_value_aed':'Expected ACV','expected_roi_multiple':'ROI','ideal_next_action':'Best Next Action'
    })


def create_decision_cards(filtered):
    top_sector, top_role, top_account, roi_leader = build_summary(filtered)
    html = f"""
    <div class='decision-strip'>
        <div class='decision-card'>
            <h5>Go-to-market wedge</h5>
            <h3>{top_role}-led offer</h3>
            <p>This role appears most often as the primary recommendation, so the front-end pitch should anchor around {top_role}-level value and keep other CXO services as add-on pathways.</p>
        </div>
        <div class='decision-card'>
            <h5>Best first sector</h5>
            <h3>{top_sector['sector']}</h3>
            <p>This sector contributes {fmt_aed(top_sector['weighted_pipeline'])} in weighted pipeline inside the current filter set, making it the best sector for initial sales focus.</p>
        </div>
        <div class='decision-card'>
            <h5>Best showcase account</h5>
            <h3>{top_account['company_name']}</h3>
            <p>Use this account as the story-led proof point: strong weighted pipeline, clear savings case, and a {top_account['win_probability']*100:.1f}% modeled win probability.</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    return top_sector, top_role, top_account, roi_leader


def account_recommendation_panel(row):
    st.markdown(f"""
    <div class='callout'>
        <strong>How to pitch this company:</strong> Lead with a <strong>{row['primary_fractional_cxo']}</strong> solution because that is the highest modeled need. Position <strong>{row['secondary_fractional_cxo']}</strong> as the expansion path, anchor the conversation on <strong>{fmt_aed(row['estimated_annual_savings_aed'])}</strong> in modeled savings versus full-time hiring, and use AI add-ons to reduce delivery cost without sacrificing breadth.
    </div>
    """, unsafe_allow_html=True)


df = load_data()
inject_css()

st.markdown("""
<div class='hero'>
    <h1>Yalla CXO</h1>
    <p>One-page executive selling dashboard for showing where fractional CXO services fit best, which accounts should be targeted first, and how the Yalla CXO model saves money compared with full-time executive hiring.</p>
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

top_sector, top_role, top_account, roi_leader = create_decision_cards(filtered)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric('Target accounts', f"{len(filtered)}")
k2.metric('Annual full-time cost base', fmt_aed(filtered['full_time_equivalent_cost_aed'].sum()))
k3.metric('Yalla CXO delivery cost', fmt_aed(filtered['fractional_ai_solution_cost_aed'].sum()))
k4.metric('Modeled annual savings', fmt_aed(filtered['estimated_annual_savings_aed'].sum()))
k5.metric('Average ROI multiple', f"{filtered['expected_roi_multiple'].mean():.2f}x")

st.markdown(
    f"<div class='callout'><strong>Executive recommendation:</strong> Start with a {top_role}-led proposition, focus first on {top_sector['sector']}, and use {top_account['company_name']} as the anchor case study. Across the current portfolio, the Yalla CXO model reduces modeled annual cost from {fmt_aed(filtered['full_time_equivalent_cost_aed'].sum())} under full-time hiring to {fmt_aed(filtered['fractional_ai_solution_cost_aed'].sum())}, unlocking {fmt_aed(filtered['estimated_annual_savings_aed'].sum())} in annual savings.</div>",
    unsafe_allow_html=True
)

st.markdown("<h3 class='section-title'>1. Show the economic case clearly</h3>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.altair_chart(compare_cost_chart(filtered), use_container_width=True)
    st.caption('This chart makes the buying case simple: compare the cost of hiring the equivalent executive bench full time versus using one primary fractional CXO, one secondary layer, and AI-supported delivery.')
with c2:
    st.altair_chart(savings_bridge_chart(filtered), use_container_width=True)
    st.caption('Use this value bridge to explain that savings are not an abstract benefit; they are the gap between the traditional executive staffing model and the Yalla CXO operating model.')

i1, i2 = st.columns(2)
with i1:
    insight_card('Why this saves money', f"The current filtered portfolio would cost {fmt_aed(filtered['full_time_equivalent_cost_aed'].sum())} under a full-time executive structure, versus {fmt_aed(filtered['fractional_ai_solution_cost_aed'].sum())} under Yalla CXO. That creates {fmt_aed(filtered['estimated_annual_savings_aed'].sum())} in modeled annual savings.")
with i2:
    insight_card('How to frame the pitch', f"Do not sell this as a cheaper alternative alone. Sell it as a sharper deployment model: one high-priority human CXO, one expansion-ready secondary role, and AI-supported execution for adjacent needs.")

st.markdown("<h3 class='section-title'>2. Show where the best demand sits</h3>", unsafe_allow_html=True)
c3, c4 = st.columns([1.1, 0.9])
with c3:
    st.altair_chart(value_quadrant(filtered), use_container_width=True)
    st.caption(f"Accounts in the upper-right are your best live selling opportunities because they combine stronger savings with stronger weighted pipeline value. {top_account['company_name']} is currently the clearest example in the selected portfolio.")
with c4:
    st.altair_chart(sector_role_heatmap(filtered), use_container_width=True)
    heat = filtered.groupby('sector')[['cfo_need_score','cto_need_score','chro_need_score','cmo_need_score','coo_need_score']].mean().stack().sort_values(ascending=False)
    hotspot = heat.index[0]
    st.caption(f"Most actionable hotspot: {hotspot[0]} shows the strongest average demand for {hotspot[1].replace('_need_score','').upper()}. That is where sector-specific messaging should start.")

i3, i4 = st.columns(2)
with i3:
    insight_card('What to prioritize first', f"Lead generation should start with {top_sector['sector']} because it carries the strongest weighted pipeline concentration. Within that sector, lead with {top_role} pain as the opening commercial narrative.")
with i4:
    insight_card('How to package the solution', 'Build the offer as a primary CXO-led intervention with secondary expansion and AI-supported delivery. This makes the proposition easier to understand and easier to buy than a broad multi-executive consulting pitch.')

st.markdown("<h3 class='section-title'>3. Show the forward revenue projection</h3>", unsafe_allow_html=True)
c5, c6 = st.columns([0.95, 1.05])
with c5:
    st.altair_chart(projection_chart(filtered), use_container_width=True)
    st.caption('This projection converts the opportunity set into a commercial story: current annual contract potential, near-term forecast, and longer-term lifetime value.')
with c6:
    top_table = top_accounts_table(filtered, 12)
    st.subheader('Best accounts to pitch now')
    st.dataframe(top_table, use_container_width=True, hide_index=True)

i5, i6 = st.columns(2)
with i5:
    insight_card('Best showcase company', f"{top_account['company_name']} should be used as the flagship example because it combines a strong savings case, attractive contract value, and a clear next action of '{top_account['ideal_next_action']}'.")
with i6:
    insight_card('Best ROI proof point', f"{roi_leader['company_name']} has the strongest modeled ROI at {roi_leader['expected_roi_multiple']:.2f}x. Use accounts like this when the buyer is cost-sensitive and needs a rapid economic justification.")

st.markdown("<h3 class='section-title'>4. Turn the page into a live pitch tool</h3>", unsafe_allow_html=True)
selected = st.selectbox('Select a company to personalize the pitch', filtered.sort_values('company_name')['company_name'].tolist(), index=0)
row = filtered.loc[filtered['company_name'] == selected].iloc[0]
account_recommendation_panel(row)

c7, c8 = st.columns([0.55, 0.45])
with c7:
    st.markdown(f"""
    ### {row['company_name']}
    **Sector:** {row['sector']}  
    **Primary CXO to lead with:** {row['primary_fractional_cxo']}  
    **Secondary expansion path:** {row['secondary_fractional_cxo']}  
    **Expected ACV:** {fmt_aed(row['expected_annual_contract_value_aed'])}  
    **Expected LTV:** {fmt_aed(row['expected_account_ltv_aed'])}  
    **Modeled annual savings:** {fmt_aed(row['estimated_annual_savings_aed'])} ({row['estimated_savings_pct']:.1f}%)  
    **Win probability:** {row['win_probability']*100:.1f}%  
    **Ideal next action:** {row['ideal_next_action']}  
    **AI-supported roles:** {row['ai_supported_roles']}  
    **AI add-ons:** {row['ai_agent_addons']}
    """)
    role_scores = pd.DataFrame({'Role':['CFO','CTO','CHRO','CMO','COO'], 'Need Score':[row['cfo_need_score'],row['cto_need_score'],row['chro_need_score'],row['cmo_need_score'],row['coo_need_score']]})
    role_scores = role_scores.sort_values('Need Score', ascending=False)
    role_chart = alt.Chart(role_scores).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x='Role:N', y=alt.Y('Need Score:Q', title='Need Score'), color='Role:N', tooltip=['Role','Need Score']
    ).properties(title='Why this company gets this recommendation', height=320)
    st.altair_chart(role_chart, use_container_width=True)
with c8:
    one_company = pd.DataFrame({
        'Cost Type':['Full-time equivalent','Yalla CXO model','Savings'],
        'Value':[row['full_time_equivalent_cost_aed'], row['fractional_ai_solution_cost_aed'], row['estimated_annual_savings_aed']],
        'Type':['Base','Residual','Savings']
    })
    single_cost = alt.Chart(one_company).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x='Cost Type:N', y=alt.Y('Value:Q', title='AED'), color=alt.Color('Type:N', scale=alt.Scale(domain=['Base','Residual','Savings'], range=['#94A3B8','#0B6B3A','#00B14F']), title=''), tooltip=['Cost Type', alt.Tooltip('Value:Q', format=',.0f')]
    ).properties(title='Company-level cost story', height=320)
    st.altair_chart(single_cost, use_container_width=True)
    insight_card('Suggested talk track', f"Open with the savings delta of {fmt_aed(row['estimated_annual_savings_aed'])}, then explain why {row['primary_fractional_cxo']} is the lead role today. After that, position {row['secondary_fractional_cxo']} and the AI add-ons as the low-friction expansion path once the first intervention proves value.")

st.download_button('Download filtered dataset', filtered.to_csv(index=False).encode('utf-8'), file_name='yalla_cxo_filtered.csv', mime='text/csv')
