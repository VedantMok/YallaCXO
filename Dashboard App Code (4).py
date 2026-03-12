import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.set_page_config(page_title="Yalla CXO", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fractional_cxo_dubai_top100_framework_ready.csv")


def fmt_aed(x):
    if pd.isna(x):
        return "-"
    x = float(x)
    if abs(x) >= 1_000_000_000:
        return f"AED {x/1_000_000_000:.2f}B"
    if abs(x) >= 1_000_000:
        return f"AED {x/1_000_000:.2f}M"
    if abs(x) >= 1_000:
        return f"AED {x/1_000:.1f}K"
    return f"AED {x:,.0f}"


def top_n_table(df, n=15):
    cols = [
        "company_name", "sector", "primary_fractional_cxo", "secondary_fractional_cxo",
        "urgency_tier", "estimated_annual_savings_aed", "expected_annual_contract_value_aed",
        "expected_account_ltv_aed", "win_probability", "ideal_next_action"
    ]
    t = df.sort_values(["weighted_pipeline_value_aed", "urgency_score"], ascending=False)[cols].head(n).copy()
    t["estimated_annual_savings_aed"] = t["estimated_annual_savings_aed"].map(fmt_aed)
    t["expected_annual_contract_value_aed"] = t["expected_annual_contract_value_aed"].map(fmt_aed)
    t["expected_account_ltv_aed"] = t["expected_account_ltv_aed"].map(fmt_aed)
    t["win_probability"] = (t["win_probability"] * 100).round(1).astype(str) + "%"
    return t.rename(columns={
        "company_name": "Company",
        "sector": "Sector",
        "primary_fractional_cxo": "Primary CXO",
        "secondary_fractional_cxo": "Secondary CXO",
        "urgency_tier": "Urgency",
        "estimated_annual_savings_aed": "Savings",
        "expected_annual_contract_value_aed": "Expected ACV",
        "expected_account_ltv_aed": "Expected LTV",
        "win_probability": "Win Prob.",
        "ideal_next_action": "Next Action"
    })


def scatter_chart(df):
    return alt.Chart(df).mark_circle(opacity=0.8).encode(
        x=alt.X('estimated_annual_savings_aed:Q', title='Estimated Annual Savings (AED)'),
        y=alt.Y('expected_annual_contract_value_aed:Q', title='Expected Annual Contract Value (AED)'),
        size=alt.Size('urgency_score:Q', title='Urgency Score', scale=alt.Scale(range=[60, 1000])),
        color=alt.Color('primary_fractional_cxo:N', title='Primary CXO'),
        tooltip=['company_name', 'sector', 'primary_fractional_cxo', 'secondary_fractional_cxo', 'urgency_tier', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed']
    ).properties(title='Savings vs Expected Contract Value', height=420)


def heatmap_roles(df):
    role_cols = ['cfo_need_score', 'cto_need_score', 'chro_need_score', 'cmo_need_score', 'coo_need_score']
    role_names = ['CFO', 'CTO', 'CHRO', 'CMO', 'COO']
    h = df.groupby('sector')[role_cols].mean().reset_index()
    h.columns = ['sector'] + role_names
    melted = h.melt('sector', var_name='Role', value_name='Avg Need Score')
    base = alt.Chart(melted).encode(
        x=alt.X('Role:N', title='Role'),
        y=alt.Y('sector:N', title='Sector', sort='-x')
    )
    heat = base.mark_rect().encode(
        color=alt.Color('Avg Need Score:Q', scale=alt.Scale(scheme='yellowgreenblue')),
        tooltip=['sector', 'Role', alt.Tooltip('Avg Need Score:Q', format='.1f')]
    )
    text = base.mark_text(size=11).encode(text=alt.Text('Avg Need Score:Q', format='.1f'))
    return (heat + text).properties(title='Average CXO Need Score by Sector', height=460)


def bar_primary(df):
    s = df['primary_fractional_cxo'].value_counts().reset_index()
    s.columns = ['Primary CXO', 'Count']
    return alt.Chart(s).mark_bar().encode(
        x=alt.X('Primary CXO:N', sort='-y'),
        y='Count:Q',
        color='Primary CXO:N',
        tooltip=['Primary CXO', 'Count']
    ).properties(title='Primary CXO Demand Distribution', height=380)


def bar_sector_value(df):
    s = df.groupby('sector', as_index=False).agg(
        weighted_pipeline_value_aed=('weighted_pipeline_value_aed', 'sum'),
        expected_account_ltv_aed=('expected_account_ltv_aed', 'mean')
    ).sort_values('weighted_pipeline_value_aed', ascending=False)
    return alt.Chart(s).mark_bar().encode(
        x=alt.X('weighted_pipeline_value_aed:Q', title='Weighted Pipeline Value (AED)'),
        y=alt.Y('sector:N', sort='-x', title='Sector'),
        color=alt.Color('expected_account_ltv_aed:Q', scale=alt.Scale(scheme='tealblues'), title='Avg LTV'),
        tooltip=['sector', 'weighted_pipeline_value_aed', 'expected_account_ltv_aed']
    ).properties(title='Weighted Pipeline by Sector', height=460)


def funnel_stage(df):
    stage_order = ['Prospect', 'Qualified', 'Discovery', 'Proposal', 'Negotiation', 'Pilot']
    s = df.groupby('pipeline_stage', as_index=False).agg(accounts=('company_id', 'count'), pipeline=('weighted_pipeline_value_aed', 'sum'))
    s['pipeline_stage'] = pd.Categorical(s['pipeline_stage'], categories=stage_order, ordered=True)
    s = s.sort_values('pipeline_stage')
    return alt.Chart(s).mark_bar().encode(
        x=alt.X('accounts:Q', title='Accounts'),
        y=alt.Y('pipeline_stage:N', sort=stage_order, title='Stage'),
        color=alt.Color('pipeline:Q', scale=alt.Scale(scheme='greens'), title='Weighted Pipeline'),
        tooltip=['pipeline_stage', 'accounts', 'pipeline']
    ).properties(title='Pipeline Stage Funnel View', height=380)


def box_roi(df):
    return alt.Chart(df).mark_boxplot(extent='min-max').encode(
        x=alt.X('primary_fractional_cxo:N', title='Primary CXO'),
        y=alt.Y('expected_roi_multiple:Q', title='ROI Multiple'),
        color='primary_fractional_cxo:N',
        tooltip=['primary_fractional_cxo', 'expected_roi_multiple']
    ).properties(title='ROI Distribution by Primary CXO', height=380)


def segment_mix(df):
    s = df.groupby(['maturity_segment', 'pain_archetype'], as_index=False).size()
    return alt.Chart(s).mark_bar().encode(
        x=alt.X('maturity_segment:N', title='Maturity Segment'),
        y=alt.Y('size:Q', title='Company Count'),
        color=alt.Color('pain_archetype:N', title='Pain Archetype'),
        tooltip=['maturity_segment', 'pain_archetype', 'size']
    ).properties(title='Segmentation Mix', height=420)


def outbound_uplift(df):
    s = df.groupby(['offer_type', 'treatment_flag'], as_index=False).agg(response_probability=('response_probability', 'mean'))
    s['treatment_flag'] = s['treatment_flag'].map({0: 'Baseline', 1: 'Treatment'})
    return alt.Chart(s).mark_bar().encode(
        x=alt.X('offer_type:N', title='Offer Type'),
        y=alt.Y('response_probability:Q', title='Response Probability', axis=alt.Axis(format='%')),
        color=alt.Color('treatment_flag:N', title='Group'),
        xOffset='treatment_flag:N',
        tooltip=['offer_type', 'treatment_flag', alt.Tooltip('response_probability:Q', format='.1%')]
    ).properties(title='Response Probability by Offer and Treatment', height=380)


def account_detail_card(row):
    st.markdown(f"""
    ### {row['company_name']}
    **Sector:** {row['sector']}  
    **Primary recommendation:** {row['primary_fractional_cxo']}  
    **Secondary recommendation:** {row['secondary_fractional_cxo']}  
    **Urgency:** {row['urgency_tier']} ({row['urgency_score']:.1f})  
    **Expected ACV:** {fmt_aed(row['expected_annual_contract_value_aed'])}  
    **Expected LTV:** {fmt_aed(row['expected_account_ltv_aed'])}  
    **Estimated savings:** {fmt_aed(row['estimated_annual_savings_aed'])} ({row['estimated_savings_pct']:.1f}%)  
    **Win probability:** {row['win_probability']*100:.1f}%  
    **Ideal next action:** {row['ideal_next_action']}  
    **AI-supported roles:** {row['ai_supported_roles']}
    """)
    role_scores = pd.DataFrame({
        'Role': ['CFO', 'CTO', 'CHRO', 'CMO', 'COO'],
        'Need Score': [row['cfo_need_score'], row['cto_need_score'], row['chro_need_score'], row['cmo_need_score'], row['coo_need_score']]
    })
    fig = alt.Chart(role_scores).mark_bar().encode(
        x='Role:N', y='Need Score:Q', color='Role:N', tooltip=['Role', 'Need Score']
    ).properties(title='Role Need Profile', height=320)
    st.altair_chart(fig, use_container_width=True)


df = load_data()

st.title('Yalla CXO')
st.caption('Dubai top-corporate targeting dashboard for identifying primary and secondary fractional CXO opportunities, expected value, and AI-supported add-ons.')

with st.sidebar:
    st.header('Filters')
    sectors = st.multiselect('Sector', sorted(df['sector'].unique()), default=sorted(df['sector'].unique()))
    roles = st.multiselect('Primary CXO', sorted(df['primary_fractional_cxo'].unique()), default=sorted(df['primary_fractional_cxo'].unique()))
    urgency = st.multiselect('Urgency Tier', sorted(df['urgency_tier'].unique()), default=sorted(df['urgency_tier'].unique()))
    tiers = st.multiselect('Account Tier', sorted(df['account_tier'].unique()), default=sorted(df['account_tier'].unique()))
    revenue_range = st.slider('Revenue (AED bn)', float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max()), (float(df['revenue_aed_bn'].min()), float(df['revenue_aed_bn'].max())))
    min_win = st.slider('Minimum Win Probability', 0.0, 1.0, 0.0, 0.01)

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

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric('Target Accounts', f'{len(filtered)}')
k2.metric('Weighted Pipeline', fmt_aed(filtered['weighted_pipeline_value_aed'].sum()))
k3.metric('Expected ACV', fmt_aed(filtered['expected_annual_contract_value_aed'].sum()))
k4.metric('Expected Savings', fmt_aed(filtered['estimated_annual_savings_aed'].sum()))
k5.metric('Avg Win Probability', f"{filtered['win_probability'].mean()*100:.1f}%")

tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Segmentation', 'Pipeline', 'Account Explorer'])

with tab1:
    c1, c2 = st.columns([1.05, 0.95])
    with c1:
        st.altair_chart(scatter_chart(filtered), use_container_width=True)
    with c2:
        st.altair_chart(bar_primary(filtered), use_container_width=True)
    c3, c4 = st.columns([1.1, 0.9])
    with c3:
        st.altair_chart(heatmap_roles(filtered), use_container_width=True)
    with c4:
        st.altair_chart(box_roi(filtered), use_container_width=True)
    st.subheader('Priority Accounts')
    st.dataframe(top_n_table(filtered, 15), use_container_width=True, hide_index=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.altair_chart(segment_mix(filtered), use_container_width=True)
    with c2:
        st.altair_chart(bar_sector_value(filtered), use_container_width=True)
    sector_summary = filtered.groupby('sector', as_index=False).agg(
        companies=('company_id', 'count'),
        avg_urgency=('urgency_score', 'mean'),
        avg_savings=('estimated_annual_savings_aed', 'mean'),
        avg_ltv=('expected_account_ltv_aed', 'mean')
    ).sort_values('avg_ltv', ascending=False)
    sector_summary['avg_urgency'] = sector_summary['avg_urgency'].round(1)
    sector_summary['avg_savings'] = sector_summary['avg_savings'].map(fmt_aed)
    sector_summary['avg_ltv'] = sector_summary['avg_ltv'].map(fmt_aed)
    st.subheader('Sector Summary')
    st.dataframe(sector_summary, use_container_width=True, hide_index=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.altair_chart(funnel_stage(filtered), use_container_width=True)
    with c2:
        st.altair_chart(outbound_uplift(filtered), use_container_width=True)
    pipeline_table = filtered.sort_values('weighted_pipeline_value_aed', ascending=False)[[
        'company_name', 'pipeline_stage', 'weighted_pipeline_value_aed', 'forecast_2q_revenue_aed',
        'response_probability', 'win_probability', 'expected_close_days', 'ideal_next_action'
    ]].copy()
    pipeline_table['weighted_pipeline_value_aed'] = pipeline_table['weighted_pipeline_value_aed'].map(fmt_aed)
    pipeline_table['forecast_2q_revenue_aed'] = pipeline_table['forecast_2q_revenue_aed'].map(fmt_aed)
    pipeline_table['response_probability'] = (pipeline_table['response_probability'] * 100).round(1).astype(str) + '%'
    pipeline_table['win_probability'] = (pipeline_table['win_probability'] * 100).round(1).astype(str) + '%'
    pipeline_table = pipeline_table.rename(columns={
        'company_name': 'Company', 'pipeline_stage': 'Stage', 'weighted_pipeline_value_aed': 'Weighted Pipeline',
        'forecast_2q_revenue_aed': '2Q Forecast', 'response_probability': 'Response Prob.',
        'win_probability': 'Win Prob.', 'expected_close_days': 'Close Days', 'ideal_next_action': 'Next Action'
    })
    st.subheader('Pipeline Detail')
    st.dataframe(pipeline_table, use_container_width=True, hide_index=True)

with tab4:
    selected = st.selectbox('Select company', filtered.sort_values('company_name')['company_name'].tolist())
    row = filtered.loc[filtered['company_name'] == selected].iloc[0]
    c1, c2 = st.columns([0.55, 0.45])
    with c1:
        account_detail_card(row)
    with c2:
        detail_cols = [
            'revenue_aed_bn', 'revenue_growth_12m_pct', 'employee_count', 'digital_maturity_score',
            'cash_flow_volatility_score', 'process_efficiency_score', 'attrition_rate_pct',
            'campaign_roi_x', 'expected_roi_multiple', 'next_service_expansion_days'
        ]
        detail = pd.DataFrame({'Metric': detail_cols, 'Value': [row[c] for c in detail_cols]})
        fig = alt.Chart(detail).mark_bar().encode(
            x=alt.X('Value:Q', title='Value'),
            y=alt.Y('Metric:N', sort='-x', title='Metric'),
            tooltip=['Metric', 'Value']
        ).properties(title='Company Metrics Snapshot', height=420)
        st.altair_chart(fig, use_container_width=True)
        st.markdown('### AI Add-ons')
        st.write(row['ai_agent_addons'])

st.download_button(
    'Download filtered dataset',
    filtered.to_csv(index=False).encode('utf-8'),
    file_name='yalla_cxo_filtered.csv',
    mime='text/csv'
)
