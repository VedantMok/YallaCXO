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
    .main {background: linear-gradient(180deg, #F8FCFA 0%, #FFFFFF 30%);}    
    .hero {
        background: linear-gradient(135deg, #0B6B3A 0%, #00B14F 55%, #5CE39A 100%);
        padding: 1.25rem 1.4rem;
        border-radius: 22px;
        color: white;
        box-shadow: 0 14px 34px rgba(0,177,79,.18);
        margin-bottom: 1rem;
    }
    .hero h1 {margin:0; font-size:2rem;}
    .hero p {margin:.35rem 0 0 0; opacity:.95;}
    .mini-note {
        background:#F4FBF7; border:1px solid #D9EFE3; border-radius:16px; padding:.9rem 1rem; margin:.35rem 0 1rem 0;
    }
    .mini-note strong {color:#0B6B3A;}
    .insight-box {
        background:#FFFFFF; border:1px solid #E2EFE8; border-left:5px solid #00B14F; border-radius:16px; padding:1rem 1rem .9rem 1rem;
        box-shadow:0 8px 18px rgba(0,0,0,.03); height:100%;
    }
    .insight-box h4 {margin:.05rem 0 .45rem 0; color:#143524;}
    .insight-box p {margin:0; color:#466454; line-height:1.5;}
    .section-title {margin-top:.2rem; color:#143524;}
    div[data-testid="stMetric"] {
        background:#FFFFFF; border:1px solid #E2EFE8; border-radius:18px; padding:.55rem .65rem; box-shadow:0 8px 18px rgba(0,0,0,.03);
    }
    .subtle {color:#607A6A; font-size:.92rem;}
    </style>
    """, unsafe_allow_html=True)


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


def pct(x):
    return f"{x*100:.1f}%"


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


def recommendation_summary(df):
    top_sector = df.groupby('sector', as_index=False)['weighted_pipeline_value_aed'].sum().sort_values('weighted_pipeline_value_aed', ascending=False).iloc[0]
    top_role = df['primary_fractional_cxo'].value_counts().idxmax()
    top_company = df.sort_values('weighted_pipeline_value_aed', ascending=False).iloc[0]
    highest_savings = df.sort_values('estimated_annual_savings_aed', ascending=False).iloc[0]
    return {
        'sector_text': f"Prioritize {top_sector['sector']} first: it contributes {fmt_aed(top_sector['weighted_pipeline_value_aed'])} in weighted pipeline across the current filter set.",
        'role_text': f"Lead with {top_role}: it appears most often as the primary recommendation, which means your core market message should anchor around this CXO pain point.",
        'account_text': f"{top_company['company_name']} is the strongest near-term account based on weighted pipeline value, with a {top_company['win_probability']*100:.1f}% win probability and {fmt_aed(top_company['expected_annual_contract_value_aed'])} expected ACV.",
        'savings_text': f"{highest_savings['company_name']} shows the largest modeled savings opportunity at {fmt_aed(highest_savings['estimated_annual_savings_aed'])}, making it ideal for a savings-led pitch."
    }


def scatter_chart(df):
    top_points = df.nlargest(min(10, len(df)), 'weighted_pipeline_value_aed').copy()
    base = alt.Chart(df).mark_circle(opacity=0.78, stroke='white', strokeWidth=0.6).encode(
        x=alt.X('estimated_annual_savings_aed:Q', title='Estimated Annual Savings (AED)'),
        y=alt.Y('expected_annual_contract_value_aed:Q', title='Expected Annual Contract Value (AED)'),
        size=alt.Size('urgency_score:Q', title='Urgency Score', scale=alt.Scale(range=[70, 900])),
        color=alt.Color('primary_fractional_cxo:N', title='Primary CXO'),
        tooltip=['company_name', 'sector', 'primary_fractional_cxo', 'secondary_fractional_cxo', 'urgency_tier', 'estimated_annual_savings_aed', 'expected_annual_contract_value_aed', 'win_probability']
    )
    labels = alt.Chart(top_points).mark_text(align='left', dx=7, dy=-6, fontSize=10, color='#143524').encode(
        x='estimated_annual_savings_aed:Q',
        y='expected_annual_contract_value_aed:Q',
        text='company_name:N'
    )
    return (base + labels).properties(title='Savings vs Expected Contract Value', height=430)


def heatmap_roles(df):
    role_cols = ['cfo_need_score', 'cto_need_score', 'chro_need_score', 'cmo_need_score', 'coo_need_score']
    role_names = ['CFO', 'CTO', 'CHRO', 'CMO', 'COO']
    h = df.groupby('sector')[role_cols].mean().reset_index()
    h.columns = ['sector'] + role_names
    melted = h.melt('sector', var_name='Role', value_name='Avg Need Score')
    base = alt.Chart(melted).encode(
        x=alt.X('Role:N', title='Role'),
        y=alt.Y('sector:N', title='Sector', sort='-color')
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
    return alt.Chart(s).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
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
    return alt.Chart(s).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
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
    return alt.Chart(s).mark_bar(cornerRadiusEnd=8).encode(
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
    return alt.Chart(s).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X('maturity_segment:N', title='Maturity Segment'),
        y=alt.Y('size:Q', title='Company Count'),
        color=alt.Color('pain_archetype:N', title='Pain Archetype'),
        tooltip=['maturity_segment', 'pain_archetype', 'size']
    ).properties(title='Segmentation Mix', height=420)


def outbound_uplift(df):
    s = df.groupby(['offer_type', 'treatment_flag'], as_index=False).agg(response_probability=('response_probability', 'mean'))
    s['treatment_flag'] = s['treatment_flag'].map({0: 'Baseline', 1: 'Treatment'})
    return alt.Chart(s).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x=alt.X('offer_type:N', title='Offer Type'),
        y=alt.Y('response_probability:Q', title='Response Probability', axis=alt.Axis(format='%')),
        color=alt.Color('treatment_flag:N', title='Group'),
        xOffset='treatment_flag:N',
        tooltip=['offer_type', 'treatment_flag', alt.Tooltip('response_probability:Q', format='.1%')]
    ).properties(title='Response Probability by Offer and Treatment', height=380)


def role_action_text(df):
    role = df['primary_fractional_cxo'].value_counts().idxmax()
    subset = df[df['primary_fractional_cxo'] == role]
    top_sector = subset.groupby('sector')['weighted_pipeline_value_aed'].sum().sort_values(ascending=False).index[0]
    avg_save = subset['estimated_annual_savings_aed'].mean()
    return f"Most urgent commercial motion: build a {role}-led offer first, especially for {top_sector}, where that role concentrates the strongest weighted demand. Average modeled savings for these accounts is {fmt_aed(avg_save)}."


def stage_action_text(df):
    pilot = df[df['pipeline_stage'].isin(['Negotiation', 'Pilot'])]
    if len(pilot) == 0:
        return "The current filter set is still early-stage, so the main task is to increase discovery and proposal volume before pushing for pilots."
    return f"Near-term conversion focus: {len(pilot)} accounts already sit in Negotiation or Pilot, representing {fmt_aed(pilot['weighted_pipeline_value_aed'].sum())} in weighted pipeline. Prioritize tailored commercial proposals and pilot-to-retainer conversion."


def uplift_action_text(df):
    uplift = df.groupby(['offer_type', 'treatment_flag'], as_index=False)['response_probability'].mean()
    pivot = uplift.pivot(index='offer_type', columns='treatment_flag', values='response_probability').fillna(0)
    pivot['lift'] = pivot.get(1, 0) - pivot.get(0, 0)
    best = pivot['lift'].idxmax()
    return f"Best message-offer pattern: '{best}' produces the strongest treatment lift in modeled response probability, so this should be the default hook in outbound testing."


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
    **Service mix:** {row['service_mix']}  
    **AI-supported roles:** {row['ai_supported_roles']}
    """)
    role_scores = pd.DataFrame({
        'Role': ['CFO', 'CTO', 'CHRO', 'CMO', 'COO'],
        'Need Score': [row['cfo_need_score'], row['cto_need_score'], row['chro_need_score'], row['cmo_need_score'], row['coo_need_score']]
    }).sort_values('Need Score', ascending=False)
    fig = alt.Chart(role_scores).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
        x='Role:N', y='Need Score:Q', color='Role:N', tooltip=['Role', 'Need Score']
    ).properties(title='Role Need Profile', height=320)
    st.altair_chart(fig, use_container_width=True)


def insight_card(title, text):
    st.markdown(f"<div class='insight-box'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def leader_mentions(df):
    best_value = df.sort_values('weighted_pipeline_value_aed', ascending=False).iloc[0]
    best_roi = df.sort_values('expected_roi_multiple', ascending=False).iloc[0]
    fastest_expand = df.sort_values('next_service_expansion_days').iloc[0]
    return best_value, best_roi, fastest_expand


df = load_data()
inject_css()

st.markdown("""
<div class='hero'>
    <h1>Yalla CXO</h1>
    <p>Decision dashboard for identifying the right fractional CXO, the strongest savings case, and the best AI-supported add-on path across Dubai corporates.</p>
</div>
""", unsafe_allow_html=True)

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

summary = recommendation_summary(filtered)
best_value, best_roi, fastest_expand = leader_mentions(filtered)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric('Target Accounts', f'{len(filtered)}')
k2.metric('Weighted Pipeline', fmt_aed(filtered['weighted_pipeline_value_aed'].sum()))
k3.metric('Expected ACV', fmt_aed(filtered['expected_annual_contract_value_aed'].sum()))
k4.metric('Expected Savings', fmt_aed(filtered['estimated_annual_savings_aed'].sum()))
k5.metric('Avg Win Probability', f"{filtered['win_probability'].mean()*100:.1f}%")

st.markdown(f"<div class='mini-note'><strong>Portfolio recommendation:</strong> {summary['sector_text']} {summary['role_text']}</div>", unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)
with r1:
    insight_card('Highest value account', f"{best_value['company_name']} currently leads on weighted pipeline value at {fmt_aed(best_value['weighted_pipeline_value_aed'])}. The recommended move is {best_value['ideal_next_action'].lower()}.")
with r2:
    insight_card('Best ROI case', f"{best_roi['company_name']} has the strongest modeled ROI at {best_roi['expected_roi_multiple']:.2f}x, making it ideal for a commercial proof point in your pitch narrative.")
with r3:
    insight_card('Fastest expansion path', f"{fastest_expand['company_name']} has the shortest expected next-service expansion window at {int(fastest_expand['next_service_expansion_days'])} days, which makes it a strong candidate for primary-to-secondary CXO upsell.")

tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Segmentation', 'Pipeline', 'Account Explorer'])

with tab1:
    st.markdown("<h3 class='section-title'>Commercial value landscape</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.altair_chart(scatter_chart(filtered), use_container_width=True)
        st.caption(summary['account_text'])
    with c2:
        st.altair_chart(bar_primary(filtered), use_container_width=True)
        st.caption(role_action_text(filtered))
    c3, c4 = st.columns([1.1, 0.9])
    with c3:
        st.altair_chart(heatmap_roles(filtered), use_container_width=True)
        hot = filtered.groupby('sector')[['cfo_need_score','cto_need_score','chro_need_score','cmo_need_score','coo_need_score']].mean().stack().sort_values(ascending=False)
        top_combo = hot.index[0]
        st.caption(f"Strongest sector-role hotspot: {top_combo[0]} shows the highest average demand for {top_combo[1].replace('_need_score','').upper()}, which is where sector-specific proposition design should begin.")
    with c4:
        st.altair_chart(box_roi(filtered), use_container_width=True)
        st.caption(summary['savings_text'])
    st.subheader('Priority Accounts')
    st.dataframe(top_n_table(filtered, 15), use_container_width=True, hide_index=True)

with tab2:
    st.markdown("<h3 class='section-title'>Segmentation and packaging</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.altair_chart(segment_mix(filtered), use_container_width=True)
        biggest_seg = filtered.groupby(['maturity_segment','pain_archetype']).size().sort_values(ascending=False).index[0]
        st.caption(f"Largest segment cluster: {biggest_seg[0]} companies with a dominant '{biggest_seg[1]}' pain pattern. This should guide packaging and outbound language.")
    with c2:
        st.altair_chart(bar_sector_value(filtered), use_container_width=True)
        st.caption(summary['sector_text'])
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
    i1, i2 = st.columns(2)
    with i1:
        insight_card('How to use this segment view', 'Use maturity segment to decide delivery style and pain archetype to decide the opening commercial narrative. In practice, this means you should not pitch the same CFO-led story to a digitally mature logistics firm and a transformation-gap real estate firm.')
    with i2:
        insight_card('What to do next', 'Build sector-specific landing pages and proposal templates for the top two sectors by weighted pipeline. Then tailor the primary CXO offer and the secondary AI-add-on narrative for the largest pain archetype inside each sector.')

with tab3:
    st.markdown("<h3 class='section-title'>Pipeline and response optimization</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.altair_chart(funnel_stage(filtered), use_container_width=True)
        st.caption(stage_action_text(filtered))
    with c2:
        st.altair_chart(outbound_uplift(filtered), use_container_width=True)
        st.caption(uplift_action_text(filtered))
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
    p1, p2 = st.columns(2)
    with p1:
        insight_card('Where conversion is likely', 'Accounts with both high urgency and high savings should get diagnostic-first outreach. Those accounts have a clearer economic case, which makes it easier to move them from discovery to proposal.')
    with p2:
        insight_card('Where pilots matter most', 'Use pilots for companies already in negotiation or for accounts where the primary CXO case is strong but the AI-add-on story still needs proof. That reduces perceived switching risk while preserving upsell potential.')

with tab4:
    st.markdown("<h3 class='section-title'>Account-level recommendation engine</h3>", unsafe_allow_html=True)
    selected = st.selectbox('Select company', filtered.sort_values('company_name')['company_name'].tolist())
    row = filtered.loc[filtered['company_name'] == selected].iloc[0]
    c1, c2 = st.columns([0.55, 0.45])
    with c1:
        account_detail_card(row)
        insight_card('Recommendation logic', f"This account is best approached with a {row['primary_fractional_cxo']}-led offer because it has the highest modeled need score. The {row['secondary_fractional_cxo']} recommendation should be positioned as the first expansion path, supported by AI-led add-ons where possible.")
    with c2:
        detail_cols = [
            'revenue_aed_bn', 'revenue_growth_12m_pct', 'employee_count', 'digital_maturity_score',
            'cash_flow_volatility_score', 'process_efficiency_score', 'attrition_rate_pct',
            'campaign_roi_x', 'expected_roi_multiple', 'next_service_expansion_days'
        ]
        detail = pd.DataFrame({'Metric': detail_cols, 'Value': [row[c] for c in detail_cols]})
        fig = alt.Chart(detail).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
            x=alt.X('Value:Q', title='Value'),
            y=alt.Y('Metric:N', sort='-x', title='Metric'),
            tooltip=['Metric', 'Value']
        ).properties(title='Company Metrics Snapshot', height=420)
        st.altair_chart(fig, use_container_width=True)
        st.markdown('### AI Add-ons')
        st.write(row['ai_agent_addons'])
        st.markdown(f"<div class='mini-note'><strong>Action recommendation:</strong> Start with {row['ideal_next_action'].lower()}, anchor the pitch on {fmt_aed(row['estimated_annual_savings_aed'])} in estimated savings, and frame the AI add-ons as support for {row['secondary_fractional_cxo']}-related execution.</div>", unsafe_allow_html=True)

st.download_button(
    'Download filtered dataset',
    filtered.to_csv(index=False).encode('utf-8'),
    file_name='yalla_cxo_filtered.csv',
    mime='text/csv'
)
