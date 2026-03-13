
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="Yalla CXO", page_icon="🧭", layout="wide")

ROLE_COLS = {
    "CFO": "cfo_need_score",
    "CTO": "cto_need_score",
    "CHRO": "chro_need_score",
    "CMO": "cmo_need_score",
    "COO": "coo_need_score",
}

ARCHETYPE_MAP = {
    "CFO": "Finance-stressed",
    "CTO": "Tech-transformation",
    "CHRO": "People-scaling",
    "CMO": "Marketing-efficiency",
    "COO": "Operational-efficiency",
}

ZONE_DATA = {
    "DIFC": (25.2137, 55.2796, "Dubai's core financial district with strong strategy and finance demand."),
    "Downtown Dubai": (25.1972, 55.2744, "High-visibility corporate zone with complex growth and operating needs."),
    "Business Bay": (25.1860, 55.2708, "Dense commercial corridor where finance, marketing, and COO work often intersect."),
    "Dubai Internet City": (25.0955, 55.1570, "Technology-focused cluster with digital transformation and CTO-led demand."),
    "Dubai Media City": (25.0951, 55.1562, "Brand-heavy hub where commercial growth and marketing execution matter."),
    "Jumeirah Lakes Towers": (25.0674, 55.1404, "Mixed business cluster with varied operating and people-management needs."),
    "Dubai Silicon Oasis": (25.1194, 55.3773, "Innovation-oriented district suited to systems and scale-up narratives."),
    "Dubai South": (24.8968, 55.1614, "Logistics and expansion corridor with execution and operating-model importance."),
    "Al Quoz": (25.1394, 55.2278, "Industrial and operating-heavy area with efficiency and cost-control relevance."),
    "Jebel Ali": (24.9857, 55.0657, "Trade and industrial base where COO and CFO interventions often resonate."),
}

SECTOR_ZONE_MAP = {
    "Financial Services": "DIFC",
    "Banking": "DIFC",
    "Insurance": "DIFC",
    "Real Estate": "Downtown Dubai",
    "Hospitality": "Downtown Dubai",
    "Technology": "Dubai Internet City",
    "Media": "Dubai Media City",
    "Telecommunications": "Dubai Internet City",
    "Retail": "Business Bay",
    "E-commerce": "Business Bay",
    "Healthcare": "Business Bay",
    "Education": "Jumeirah Lakes Towers",
    "Industrial": "Jebel Ali",
    "Logistics": "Dubai South",
    "Manufacturing": "Al Quoz",
    "Energy": "Jebel Ali",
}

PALETTE = {
    "bg": "#08111F",
    "panel": "#101B2D",
    "panel_2": "#0D1728",
    "border": "rgba(255,255,255,0.08)",
    "text": "#E5EEF9",
    "muted": "#8FA5C2",
    "blue": "#5AA9FF",
    "teal": "#2DD4BF",
    "violet": "#A78BFA",
    "amber": "#FBBF24",
    "red": "#FB7185",
    "grid": "rgba(255,255,255,0.08)",
}


@st.cache_data
def load_data():
    candidates = [
        "Fractional-CXO-Dubai-Top-100-Framework-enhanced.csv",
        "Fractional-CXO-Dubai-Top-100-Framework.csv",
        "fractional_cxo_dubai_top100_framework_ready.csv",
    ]
    for path in candidates:
        try:
            return pd.read_csv(path)
        except Exception:
            pass
    raise FileNotFoundError("No supported CSV file found.")


def safe_series(df, col, default=0.0):
    if col not in df.columns:
        return pd.Series([default] * len(df), index=df.index)
    return df[col]


def safe_value(row, col, default=0.0):
    return row[col] if col in row.index and pd.notna(row[col]) else default


def aed(x):
    x = float(x)
    if abs(x) >= 1_000_000_000:
        return f"AED {x/1_000_000_000:.2f}B"
    if abs(x) >= 1_000_000:
        return f"AED {x/1_000_000:.2f}M"
    if abs(x) >= 1_000:
        return f"AED {x/1_000:.1f}K"
    return f"AED {x:,.0f}"


def role_order(row):
    scores = {role: float(safe_value(row, col, 0.0)) for role, col in ROLE_COLS.items()}
    if sum(scores.values()) == 0:
        primary = str(safe_value(row, "primary_fractional_cxo", "CFO"))
        secondary = str(safe_value(row, "secondary_fractional_cxo", "CTO"))
        return [(primary, float(safe_value(row, "primary_need_score", 70))), (secondary, float(safe_value(row, "secondary_need_score", 60))), ("COO", 50), ("CHRO", 45), ("CMO", 40)]
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def enrich_locations(df):
    out = df.copy()
    zones = list(ZONE_DATA.keys())
    if "hq_zone" not in out.columns:
        out["hq_zone"] = out["sector"].map(SECTOR_ZONE_MAP)
        out["hq_zone"] = out["hq_zone"].fillna(out["company_name"].apply(lambda x: zones[abs(hash(str(x))) % len(zones)]))
    if "hq_zone_context" not in out.columns:
        out["hq_zone_context"] = out["hq_zone"].map(lambda z: ZONE_DATA.get(z, ZONE_DATA["Business Bay"])[2])
    if "city" not in out.columns:
        out["city"] = "Dubai"
    if "region" not in out.columns:
        out["region"] = "Dubai"
    if "country" not in out.columns:
        out["country"] = "UAE"
    if "latitude" not in out.columns:
        out["latitude"] = out["hq_zone"].map(lambda z: ZONE_DATA.get(z, ZONE_DATA["Business Bay"])[0])
        out["latitude"] = out["latitude"] + out["company_name"].apply(lambda x: ((abs(hash(str(x) + 'lat')) % 100) - 50) * 0.00025)
    if "longitude" not in out.columns:
        out["longitude"] = out["hq_zone"].map(lambda z: ZONE_DATA.get(z, ZONE_DATA["Business Bay"])[1])
        out["longitude"] = out["longitude"] + out["company_name"].apply(lambda x: ((abs(hash(str(x) + 'lon')) % 100) - 50) * 0.00025)
    return out


def derive_fields(df):
    out = enrich_locations(df)
    primary_roles, secondary_roles, primary_scores, secondary_scores, contexts = [], [], [], [], []
    for _, row in out.iterrows():
        ordered = role_order(row)
        pr, ps = ordered[0]
        sr, ss = ordered[1]
        primary_roles.append(pr)
        secondary_roles.append(sr)
        primary_scores.append(float(ps))
        secondary_scores.append(float(ss))
        sector = str(safe_value(row, "sector", "diversified"))
        revenue_band = str(safe_value(row, "revenue_band", "large-enterprise range"))
        urgency = str(safe_value(row, "urgency_tier", "active"))
        contexts.append(
            f"A Dubai-based {sector.lower()} company in the {revenue_band.lower()}, showing {urgency.lower()} pressure; a {pr}-led engagement is the clearest entry point, with {sr} as the strongest expansion path."
        )
    if "company_context_line" not in out.columns:
        out["company_context_line"] = contexts

    out["primary_role_derived"] = primary_roles
    out["secondary_role_derived"] = secondary_roles
    out["primary_role_score"] = primary_scores
    out["secondary_role_score"] = secondary_scores
    out["need_archetype_derived"] = out["primary_role_derived"].map(ARCHETYPE_MAP)
    out["win_probability"] = pd.to_numeric(safe_series(out, "win_probability"), errors="coerce").fillna(0)
    out["response_probability"] = pd.to_numeric(safe_series(out, "response_probability"), errors="coerce").fillna(0)
    out["expected_annual_contract_value_aed"] = pd.to_numeric(safe_series(out, "expected_annual_contract_value_aed"), errors="coerce").fillna(0)
    out["expected_account_ltv_aed"] = pd.to_numeric(safe_series(out, "expected_account_ltv_aed"), errors="coerce").fillna(0)
    out["estimated_annual_savings_aed"] = pd.to_numeric(safe_series(out, "estimated_annual_savings_aed"), errors="coerce").fillna(0)
    out["full_time_equivalent_cost_aed"] = pd.to_numeric(safe_series(out, "full_time_equivalent_cost_aed"), errors="coerce").fillna(0)
    out["fractional_ai_solution_cost_aed"] = pd.to_numeric(safe_series(out, "fractional_ai_solution_cost_aed"), errors="coerce").fillna(0)
    out["urgency_score"] = pd.to_numeric(safe_series(out, "urgency_score"), errors="coerce").fillna(0)
    out["account_health_score"] = pd.to_numeric(safe_series(out, "account_health_score"), errors="coerce").fillna(0)
    out["expected_close_days"] = pd.to_numeric(safe_series(out, "expected_close_days"), errors="coerce").fillna(60)
    out["revenue_aed_bn"] = pd.to_numeric(safe_series(out, "revenue_aed_bn"), errors="coerce").fillna(0)
    out["client_churn_risk_score"] = pd.to_numeric(safe_series(out, "client_churn_risk_score"), errors="coerce").fillna(0)

    out["win_pct"] = out["win_probability"] * 100
    out["response_pct"] = out["response_probability"] * 100
    out["weighted_acv"] = out["expected_annual_contract_value_aed"] * out["win_probability"]
    out["weighted_ltv"] = out["expected_account_ltv_aed"] * out["win_probability"]
    out["cost_gap_vs_full_time"] = out["full_time_equivalent_cost_aed"] - out["fractional_ai_solution_cost_aed"]
    out["value_at_risk"] = out["expected_account_ltv_aed"] * out["client_churn_risk_score"] / 100.0
    out["roi_proxy"] = out["estimated_annual_savings_aed"] / out["fractional_ai_solution_cost_aed"].replace(0, np.nan)
    out["roi_proxy"] = out["roi_proxy"].replace([np.inf, -np.inf], np.nan).fillna(0)
    out["priority_index"] = (
        0.28 * out["primary_role_score"]
        + 0.22 * out["urgency_score"]
        + 0.20 * out["win_pct"]
        + 0.15 * out["response_pct"]
        + 0.15 * out["account_health_score"]
    )
    out["close_month"] = np.clip(np.ceil(out["expected_close_days"] / 30), 1, 6).astype(int)
    out["close_month_label"] = "M" + out["close_month"].astype(str)
    out["priority_band"] = pd.qcut(out["priority_index"].rank(method="first"), 4, labels=["Watch", "Build", "Prioritize", "Act now"])
    return out


def apply_style():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');
        html, body, [class*="css"] {{font-family:'Inter', sans-serif;}}
        .stApp {{background:
            radial-gradient(circle at 10% 10%, rgba(90,169,255,0.14), transparent 25%),
            radial-gradient(circle at 90% 5%, rgba(45,212,191,0.12), transparent 22%),
            linear-gradient(180deg, #08111F 0%, #0B1424 100%);
            color:{PALETTE['text']};
        }}
        [data-testid="stSidebar"] {{display:none;}}
        .block-container {{padding-top:0.9rem; max-width:1500px;}}
        .topbar {{background:rgba(16,27,45,0.78); border:1px solid {PALETTE['border']}; border-radius:24px; padding:1.1rem 1.2rem; box-shadow:0 18px 50px rgba(0,0,0,0.28); margin-bottom:0.85rem; backdrop-filter:blur(14px);}}
        .brand {{font-family:'Space Grotesk', sans-serif; font-size:2rem; font-weight:700; color:{PALETTE['text']}; margin:0;}}
        .sub {{margin:0.35rem 0 0 0; color:{PALETTE['muted']}; line-height:1.55; max-width:1000px;}}
        .controls {{background:rgba(16,27,45,0.70); border:1px solid {PALETTE['border']}; border-radius:22px; padding:0.9rem 1rem; margin-bottom:0.85rem;}}
        .mapwrap {{background:rgba(16,27,45,0.72); border:1px solid {PALETTE['border']}; border-radius:24px; padding:0.8rem 0.8rem 0.55rem 0.8rem; margin-bottom:0.85rem;}}
        .hero {{background:linear-gradient(135deg, rgba(90,169,255,0.16), rgba(45,212,191,0.12)); border:1px solid {PALETTE['border']}; border-radius:24px; padding:1.05rem 1.1rem; margin-bottom:0.85rem;}}
        .hero h2 {{font-family:'Space Grotesk', sans-serif; margin:0; color:{PALETTE['text']}; font-size:1.75rem;}}
        .hero p {{margin:0.45rem 0 0 0; color:{PALETTE['muted']}; line-height:1.55; max-width:980px;}}
        .chiprow {{display:flex; flex-wrap:wrap; gap:0.45rem; margin-top:0.85rem;}}
        .chip {{display:inline-flex; padding:0.4rem 0.7rem; border-radius:999px; background:rgba(255,255,255,0.06); border:1px solid {PALETTE['border']}; color:{PALETTE['text']}; font-size:0.8rem;}}
        .metric {{background:rgba(16,27,45,0.78); border:1px solid {PALETTE['border']}; border-radius:20px; padding:0.95rem 0.95rem; min-height:118px; box-shadow:0 16px 40px rgba(0,0,0,0.22);}}
        .metric .label {{font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:{PALETTE['muted']}; margin-bottom:0.28rem;}}
        .metric .value {{font-family:'Space Grotesk', sans-serif; font-size:1.42rem; font-weight:700; color:{PALETTE['text']}; line-height:1.08; margin-bottom:0.2rem;}}
        .metric .subv {{font-size:0.84rem; color:{PALETTE['muted']}; line-height:1.42;}}
        .section {{background:rgba(16,27,45,0.72); border:1px solid {PALETTE['border']}; border-radius:24px; padding:1rem 1rem 0.2rem 1rem; margin-bottom:0.95rem;}}
        .section h3 {{font-family:'Space Grotesk', sans-serif; margin:0; color:{PALETTE['text']}; font-size:1.22rem;}}
        .section p {{margin:0.25rem 0 0.9rem 0; color:{PALETTE['muted']}; line-height:1.55; max-width:980px;}}
        .note {{background:rgba(255,255,255,0.04); border:1px solid {PALETTE['border']}; border-radius:16px; padding:0.85rem 0.9rem; color:{PALETTE['text']}; min-height:118px;}}
        .stTabs [data-baseweb="tab-list"] {{gap:0.45rem; margin-bottom:0.55rem;}}
        .stTabs [data-baseweb="tab"] {{background:rgba(16,27,45,0.72); border:1px solid {PALETTE['border']}; border-radius:14px; color:{PALETTE['muted']}; padding:0.55rem 0.85rem;}}
        .stTabs [aria-selected="true"] {{background:rgba(90,169,255,0.14); border-color:rgba(90,169,255,0.4); color:{PALETTE['text']};}}
        div[data-testid="stDataFrame"] {{border:1px solid {PALETTE['border']}; border-radius:16px; overflow:hidden;}}
        .stSelectbox label, .stSlider label, .stMultiSelect label {{color:{PALETTE['muted']} !important;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, sub):
    st.markdown(f"<div class='metric'><div class='label'>{label}</div><div class='value'>{value}</div><div class='subv'>{sub}</div></div>", unsafe_allow_html=True)


def section_open(title, copy):
    st.markdown(f"<div class='section'><h3>{title}</h3><p>{copy}</p>", unsafe_allow_html=True)


def section_close():
    st.markdown("</div>", unsafe_allow_html=True)


def plotly_theme(fig, height=350):
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=56, b=18),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=PALETTE['text'], family='Inter'),
        title_font=dict(size=18, family='Space Grotesk'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=PALETTE['muted'])),
    )
    fig.update_xaxes(showgrid=True, gridcolor=PALETTE['grid'], zeroline=False, color=PALETTE['muted'])
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE['grid'], zeroline=False, color=PALETTE['muted'])
    return fig


def top_controls(df):
    st.markdown("<div class='controls'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2.0, 1.1, 1.1, 1.2], gap='medium')
    with c2:
        sectors = ['All'] + sorted(df['sector'].dropna().unique().tolist())
        sector = st.selectbox('Sector', sectors, index=0, key='sector_main')
    with c3:
        roles = ['All'] + list(ROLE_COLS.keys())
        role = st.selectbox('Primary role', roles, index=0, key='role_main')
    with c4:
        min_win = st.slider('Min win probability', 0.0, 1.0, 0.0, 0.01, key='min_win_main')
    filtered = df.copy()
    if sector != 'All':
        filtered = filtered[filtered['sector'] == sector]
    if role != 'All':
        filtered = filtered[filtered['primary_role_derived'] == role]
    filtered = filtered[filtered['win_probability'] >= min_win].copy()
    if filtered.empty:
        st.markdown("</div>", unsafe_allow_html=True)
        return None, None
    companies = sorted(filtered['company_name'].tolist())
    current = st.session_state.get('selected_company', companies[0])
    index = companies.index(current) if current in companies else 0
    with c1:
        selected = st.selectbox('Selected company', companies, index=index, key='selected_company')
    st.markdown("</div>", unsafe_allow_html=True)
    row = filtered.loc[filtered['company_name'] == selected].iloc[0]
    return filtered, row


def static_map(filtered, row):
    keep = ['company_name', 'latitude', 'longitude', 'weighted_acv', 'primary_role_derived', 'hq_zone']
    m = filtered[keep].copy()
    m['latitude'] = pd.to_numeric(m['latitude'], errors='coerce')
    m['longitude'] = pd.to_numeric(m['longitude'], errors='coerce')
    m['weighted_acv'] = pd.to_numeric(m['weighted_acv'], errors='coerce').fillna(0)
    m = m.dropna(subset=['latitude', 'longitude'])
    if m.empty:
        st.info('Map coordinates unavailable.')
        return
    m['selected'] = m['company_name'].eq(row['company_name'])
    max_val = max(float(m['weighted_acv'].max()), 1.0)
    m['radius'] = ((m['weighted_acv'] / max_val) * 4200 + 240).clip(220, 1500)
    selected = m[m['selected']].copy()
    others = m[~m['selected']].copy()
    if selected.empty:
        selected = m.head(1).copy()
    center_lat = float(selected['latitude'].iloc[0])
    center_lon = float(selected['longitude'].iloc[0])
    st.markdown("<div class='mapwrap'>", unsafe_allow_html=True)
    st.caption(f"Dubai footprint — static map centered on {row['company_name']}; selected company highlighted in red.")
    deck = pdk.Deck(
        map_style='light',
        initial_view_state=pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=10.6, pitch=0, bearing=0),
        layers=[
            pdk.Layer(
                'ScatterplotLayer', data=others,
                get_position='[longitude, latitude]', get_radius='radius', radius_units='meters',
                radius_min_pixels=3, radius_max_pixels=12,
                get_fill_color='[96, 165, 250, 90]', get_line_color='[255,255,255,100]',
                pickable=False, stroked=True, line_width_min_pixels=1,
            ),
            pdk.Layer(
                'ScatterplotLayer', data=selected,
                get_position='[longitude, latitude]', get_radius='radius * 1.65', radius_units='meters',
                radius_min_pixels=8, radius_max_pixels=18,
                get_fill_color='[251, 113, 133, 220]', get_line_color='[255,255,255,255]',
                pickable=True, stroked=True, line_width_min_pixels=2,
            ),
        ],
        tooltip={
            'html': '<b>{company_name}</b><br/>Zone: {hq_zone}<br/>Primary role: {primary_role_derived}<br/>Weighted ACV: {weighted_acv}',
            'style': {'backgroundColor': '#0B1424', 'color': 'white'}
        },

    )
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def hero(row):
    chips = ''.join([
        f"<div class='chip'>Sector · {row['sector']}</div>",
        f"<div class='chip'>Zone · {safe_value(row, 'hq_zone', 'Dubai')}</div>",
        f"<div class='chip'>Primary · {row['primary_role_derived']}</div>",
        f"<div class='chip'>Secondary · {row['secondary_role_derived']}</div>",
        f"<div class='chip'>Archetype · {row['need_archetype_derived']}</div>",
        f"<div class='chip'>Priority · {row['priority_band']}</div>",
    ])
    st.markdown(
        f"""
        <div class='hero'>
            <h2>{row['company_name']}</h2>
            <p>{safe_value(row, 'company_context_line', 'Dubai corporate with measurable value-creation potential and a clear executive wedge.')}</p>
            <div class='chiprow'>{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def radar_chart(row):
    roles = list(ROLE_COLS.keys())
    values = [float(safe_value(row, ROLE_COLS[r], 0)) for r in roles]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=roles + [roles[0]],
        fill='toself',
        line=dict(color=PALETTE['blue'], width=3),
        fillcolor='rgba(90,169,255,0.28)',
        name='Need profile',
    ))
    fig.update_layout(
        title='Executive need profile',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(range=[0,100], gridcolor=PALETTE['grid'], tickfont=dict(color=PALETTE['muted'])),
            angularaxis=dict(gridcolor=PALETTE['grid'], tickfont=dict(color=PALETTE['text'])),
        ),
        showlegend=False,
    )
    return plotly_theme(fig, 360)


def waterfall_chart(row):
    ft = float(safe_value(row, 'full_time_equivalent_cost_aed', 0))
    frac = float(safe_value(row, 'fractional_ai_solution_cost_aed', 0))
    gap = float(safe_value(row, 'cost_gap_vs_full_time', ft - frac))
    fig = go.Figure(go.Waterfall(
        orientation='v',
        measure=['absolute', 'relative', 'total'],
        x=['Full-time cost', 'Shift to fractional + AI', 'Net gap'],
        y=[ft, -frac, 0],
        connector={'line': {'color': PALETTE['grid']}},
        increasing={'marker': {'color': PALETTE['teal']}},
        decreasing={'marker': {'color': PALETTE['red']}},
        totals={'marker': {'color': PALETTE['violet']}},
        text=[aed(ft), aed(-frac), aed(gap)],
        textposition='outside',
    ))
    fig.update_layout(title='Cost shift versus full-time hiring', showlegend=False)
    return plotly_theme(fig, 360)


def sankey_chart(row):
    sector = str(safe_value(row, 'sector', 'Sector'))
    company = str(row['company_name'])
    primary = str(row['primary_role_derived'])
    secondary = str(row['secondary_role_derived'])
    nodes = [sector, company, primary, secondary]
    idx = {n:i for i,n in enumerate(nodes)}
    val1 = max(float(safe_value(row, 'primary_role_score', 60)), 1)
    val2 = max(float(safe_value(row, 'secondary_role_score', 40)), 1)
    fig = go.Figure(go.Sankey(
        arrangement='fixed',
        node=dict(
            label=nodes,
            pad=24,
            thickness=18,
            color=[PALETTE['blue'], PALETTE['violet'], PALETTE['teal'], PALETTE['amber']],
            line=dict(color='rgba(255,255,255,0.12)', width=1),
            x=[0.02, 0.34, 0.70, 0.94],
            y=[0.45, 0.45, 0.30, 0.70],
        ),
        link=dict(
            source=[idx[sector], idx[company], idx[primary]],
            target=[idx[company], idx[primary], idx[secondary]],
            value=[val1, val1, val2],
            color=['rgba(90,169,255,0.22)', 'rgba(167,139,250,0.20)', 'rgba(45,212,191,0.20)'],
        )
    ))
    fig.update_layout(title='Recommendation flow')
    return plotly_theme(fig, 340)


def lollipop_ranking(filtered, row):
    df = filtered[['company_name', 'priority_index', 'primary_role_derived']].sort_values('priority_index', ascending=False).head(15).copy()
    selected_name = row['company_name']
    df = df.sort_values('priority_index', ascending=True)
    fig = go.Figure()
    for _, r in df.iterrows():
        color = PALETTE['red'] if r['company_name'] == selected_name else 'rgba(143,165,194,0.35)'
        width = 3 if r['company_name'] == selected_name else 1.4
        fig.add_shape(type='line', x0=0, x1=float(r['priority_index']), y0=r['company_name'], y1=r['company_name'], line=dict(color=color, width=width))
    fig.add_trace(go.Scatter(
        x=df['priority_index'], y=df['company_name'], mode='markers',
        marker=dict(size=np.where(df['company_name'].eq(selected_name), 15, 10), color=np.where(df['company_name'].eq(selected_name), PALETTE['red'], PALETTE['blue']), line=dict(color='white', width=1.2)),
        text=df['primary_role_derived'], hovertemplate='<b>%{y}</b><br>Priority: %{x:.1f}<br>Primary role: %{text}<extra></extra>'
    ))
    fig.update_layout(title='Top prioritized accounts', showlegend=False)
    return plotly_theme(fig, 390)


def quadrant_chart(filtered, row):
    df = filtered.copy()
    med_x = float(df['urgency_score'].median())
    med_y = float(df['weighted_acv'].median())
    df['selected'] = df['company_name'].eq(row['company_name'])
    fig = px.scatter(
        df, x='urgency_score', y='weighted_acv', size='estimated_annual_savings_aed',
        color='selected', color_discrete_map={True: PALETTE['red'], False: PALETTE['blue']},
        hover_name='company_name', hover_data=['sector', 'primary_role_derived', 'secondary_role_derived'],
        title='Urgency versus weighted ACV',
    )
    fig.update_traces(marker=dict(opacity=0.82, line=dict(width=1, color='white')))
    fig.add_vline(x=med_x, line_dash='dash', line_color=PALETTE['grid'])
    fig.add_hline(y=med_y, line_dash='dash', line_color=PALETTE['grid'])
    fig.add_annotation(x=med_x*1.02 if med_x != 0 else 1, y=med_y*1.02 if med_y != 0 else 1, text='High-priority zone', showarrow=False, font=dict(color=PALETTE['muted']))
    fig.update_layout(showlegend=False)
    return plotly_theme(fig, 390)


def treemap_chart(filtered):
    df = filtered.groupby(['sector', 'primary_role_derived'], as_index=False).agg(weighted_acv=('weighted_acv', 'sum'))
    fig = px.treemap(df, path=['sector', 'primary_role_derived'], values='weighted_acv', color='weighted_acv', color_continuous_scale=['#0B1424', '#2DD4BF', '#5AA9FF'], title='Portfolio value concentration')
    fig.update_layout(coloraxis_showscale=False)
    return plotly_theme(fig, 390)


def pipeline_chart(filtered):
    order = pd.DataFrame({'close_month_label': ['M1','M2','M3','M4','M5','M6']})
    df = filtered.groupby('close_month_label', as_index=False).agg(weighted_acv=('weighted_acv','sum'))
    df = order.merge(df, on='close_month_label', how='left').fillna(0)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['close_month_label'], y=df['weighted_acv'], mode='lines+markers',
        line=dict(color=PALETTE['teal'], width=3, shape='spline'),
        marker=dict(size=9, color=PALETTE['teal'], line=dict(color='white', width=1)),
        fill='tozeroy', fillcolor='rgba(45,212,191,0.18)',
        hovertemplate='%{x}<br>Weighted ACV: %{y:,.0f}<extra></extra>'
    ))
    fig.update_layout(title='Weighted pipeline pacing', showlegend=False)
    return plotly_theme(fig, 330)


def funnel_chart(row):
    touches = max(int(safe_value(row, 'sales_touchpoints_90d', 0)), 1)
    responses = max(int(round(touches * float(safe_value(row, 'response_probability', 0)) * 0.9)), 1)
    meetings = max(int(safe_value(row, 'meetings_booked_90d', 0)), 1 if responses > 1 else 0)
    proposals = max(int(safe_value(row, 'proposal_count_90d', 0)), 1 if meetings > 1 else 0)
    closes = max(float(safe_value(row, 'win_probability', 0)) * max(1, proposals), 0.5)
    fig = go.Figure(go.Funnel(
        y=['Touches', 'Responses', 'Meetings', 'Proposals', 'Expected closes'],
        x=[touches, responses, meetings, proposals, closes],
        marker={'color': [PALETTE['blue'], PALETTE['violet'], PALETTE['teal'], PALETTE['amber'], PALETTE['red']]},
        textinfo='value+percent previous'
    ))
    fig.update_layout(title='Commercial funnel', showlegend=False)
    return plotly_theme(fig, 330)


def comparables_table(filtered, row):
    df = filtered.copy()
    df['distance'] = (
        (df['revenue_aed_bn'] - row['revenue_aed_bn']).abs() * 2 +
        (df['urgency_score'] - row['urgency_score']).abs() * 0.45 +
        (df['expected_annual_contract_value_aed'] - row['expected_annual_contract_value_aed']).abs() / 500000
    )
    out = df[df['company_name'] != row['company_name']].sort_values('distance').head(8)[[
        'company_name', 'sector', 'primary_role_derived', 'weighted_acv', 'estimated_annual_savings_aed', 'priority_band'
    ]].copy()
    out['weighted_acv'] = out['weighted_acv'].map(aed)
    out['estimated_annual_savings_aed'] = out['estimated_annual_savings_aed'].map(aed)
    return out.rename(columns={
        'company_name': 'Comparable company',
        'primary_role_derived': 'Primary role',
        'weighted_acv': 'Weighted ACV',
        'estimated_annual_savings_aed': 'Savings',
        'priority_band': 'Priority band',
    })


def note_card(title, body):
    st.markdown(f"<div class='note'><strong>{title}</strong><br><br>{body}</div>", unsafe_allow_html=True)


def main():
    apply_style()
    st.markdown(
        "<div class='topbar'><div class='brand'>Yalla CXO</div><p class='sub'>A premium Dubai control tower for fractional CXO prioritization, visualized as an executive story instead of a basic analytics report.</p></div>",
        unsafe_allow_html=True,
    )

    df = derive_fields(load_data())
    filtered, row = top_controls(df)
    if filtered is None or row is None:
        st.warning('No companies match the current filters.')
        st.stop()

    static_map(filtered, row)
    hero(row)

    m1, m2, m3, m4, m5, m6 = st.columns(6, gap='medium')
    with m1:
        metric_card('Primary role', row['primary_role_derived'], f"Need score {row['primary_role_score']:.1f}")
    with m2:
        metric_card('Secondary role', row['secondary_role_derived'], f"Need score {row['secondary_role_score']:.1f}")
    with m3:
        metric_card('Expected ACV', aed(row['expected_annual_contract_value_aed']), 'Headline annual contract value')
    with m4:
        metric_card('Weighted ACV', aed(row['weighted_acv']), 'Probability-adjusted deal value')
    with m5:
        metric_card('Savings', aed(row['estimated_annual_savings_aed']), 'Annual savings versus current state')
    with m6:
        metric_card('Priority index', f"{row['priority_index']:.1f}", f"Band: {row['priority_band']}")

    t1, t2, t3 = st.tabs(['Why this company', 'Portfolio story', 'Commercial plan'])

    with t1:
        section_open('Why this company', 'Use richer visuals to explain why the selected account matters, what executive role should lead, and how the commercial logic hangs together.')
        a, b = st.columns([0.46, 0.54], gap='large')
        with a:
            st.plotly_chart(radar_chart(row), use_container_width=True, config={'displayModeBar': False})
        with b:
            st.plotly_chart(sankey_chart(row), use_container_width=True, config={'displayModeBar': False})
        c, d = st.columns([0.5, 0.5], gap='large')
        with c:
            st.plotly_chart(waterfall_chart(row), use_container_width=True, config={'displayModeBar': False})
        with d:
            st.dataframe(comparables_table(filtered, row), use_container_width=True, hide_index=True, height=360)
        e1, e2, e3 = st.columns(3, gap='large')
        with e1:
            note_card('Lead wedge', f"Start with <b>{row['primary_role_derived']}</b> because it is the strongest modeled need and the cleanest opening offer.")
        with e2:
            note_card('Expansion path', f"Use <b>{row['secondary_role_derived']}</b> as the second-stage motion after initial proof of value lands.")
        with e3:
            note_card('Location context', f"This account is mapped to <b>{safe_value(row, 'hq_zone', 'Dubai')}</b>, which fits the current portfolio geography and operating narrative.")
        section_close()

    with t2:
        section_open('Portfolio story', 'Make the selected company feel like part of a living portfolio, not an isolated row in a spreadsheet.')
        a, b = st.columns([0.52, 0.48], gap='large')
        with a:
            st.plotly_chart(lollipop_ranking(filtered, row), use_container_width=True, config={'displayModeBar': False})
        with b:
            st.plotly_chart(treemap_chart(filtered), use_container_width=True, config={'displayModeBar': False})
        st.plotly_chart(quadrant_chart(filtered, row), use_container_width=True, config={'displayModeBar': False})
        section_close()

    with t3:
        section_open('Commercial plan', 'Translate visual opportunity into timing and sales motion using weighted pipeline and funnel logic.')
        a, b = st.columns([0.52, 0.48], gap='large')
        with a:
            st.plotly_chart(pipeline_chart(filtered), use_container_width=True, config={'displayModeBar': False})
        with b:
            st.plotly_chart(funnel_chart(row), use_container_width=True, config={'displayModeBar': False})
        section_close()

    st.download_button(
        'Download filtered dataset',
        filtered.to_csv(index=False).encode('utf-8'),
        file_name='yalla_cxo_filtered.csv',
        mime='text/csv',
        use_container_width=True,
    )


if __name__ == '__main__':
    main()
