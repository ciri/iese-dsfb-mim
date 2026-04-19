import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

dash.register_page(
    __name__,
    path="/dwdaw",
    name="Customer Analytics",
)

# ── Chart styling constants ──────────────────────────────────────
CHART_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Inter, sans-serif", size=12, color="#545B64")

# ── Data (precomputed — no interactive filter on this page) ──────
df = pd.read_csv("data/Amazon-cleaned.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month_name()
df['revenue'] = df['amount_eu']

MONTH_ORDER = ['April', 'May', 'June']

# ── Cancellations & Returns ──────────────────────────────────────
cancelled = df[df['status'] == 'Cancelled']
returned  = df[df['status'] == 'Shipped - Returned to Seller']
delivered = df[~df['status'].isin(['Cancelled', 'Shipped - Returned to Seller'])]

total_orders  = len(df)
cancel_pct    = len(cancelled) / total_orders * 100
return_pct    = len(returned)  / total_orders * 100
problem_pct   = cancel_pct + return_pct

donut_fig = go.Figure(data=[go.Pie(
    labels=['Delivered / Active', 'Cancelled', 'Returned'],
    values=[len(delivered), len(cancelled), len(returned)],
    hole=0.60,
    marker_colors=['#67B346', '#FF9900', '#232F3E'],
    textinfo='percent+label',
    textfont=dict(size=12, family="Inter, sans-serif"),
    hovertemplate="%{label}: %{value:,} orders (%{percent})<extra></extra>",
    direction='clockwise',
    sort=False,
)])
donut_fig.update_layout(
    margin=dict(l=8, r=8, t=16, b=8), font=CHART_FONT,
    paper_bgcolor="#fff", showlegend=False,
    annotations=[dict(
        text=f"{total_orders:,}<br><span style='font-size:11px;color:#545B64'>total orders</span>",
        x=0.5, y=0.5,
        font=dict(size=18, color="#232F3E", family="Inter, sans-serif"),
        showarrow=False,
    )],
)

# Cancellation rate by category (top categories only)
cancel_by_cat = (
    df.assign(is_cancelled=df['status'] == 'Cancelled')
    .groupby('category')
    .agg(cancel_rate=('is_cancelled', 'mean'), order_count=('order_id', 'count'))
    .reset_index()
)
cancel_by_cat = cancel_by_cat[cancel_by_cat['order_count'] > 500].copy()
cancel_by_cat['cancel_rate_pct'] = cancel_by_cat['cancel_rate'] * 100
cancel_by_cat = cancel_by_cat.sort_values('cancel_rate_pct', ascending=True)

cancel_cat_fig = px.bar(
    cancel_by_cat, x='cancel_rate_pct', y='category', orientation='h',
    color='cancel_rate_pct',
    color_continuous_scale=[[0, '#FFE0A8'], [0.5, '#FF9900'], [1, '#CC0000']],
    template=CHART_TEMPLATE,
    custom_data=['category', 'order_count'],
)
cancel_cat_fig.update_traces(
    marker_line_width=0,
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Cancellation rate: %{x:.1f}%<br>"
        "Orders: %{customdata[1]:,}<extra></extra>"
    ),
)
cancel_cat_fig.update_layout(
    margin=dict(l=8, r=8, t=12, b=8), font=CHART_FONT,
    xaxis_title="Cancellation Rate (%)", yaxis_title="",
    plot_bgcolor="#fff", paper_bgcolor="#fff",
    showlegend=False, coloraxis_showscale=False,
)

# ── B2B vs B2C Monthly ───────────────────────────────────────────
monthly = (
    df.groupby(['month', 'B2B'])
    .agg(total_revenue=('revenue', 'sum'), order_count=('order_id', 'count'))
    .reset_index()
)
monthly['B2B'] = monthly['B2B'].replace({True: 'B2B', False: 'B2C'})
monthly['month'] = pd.Categorical(monthly['month'], categories=MONTH_ORDER, ordered=True)
monthly = monthly.sort_values('month')

b2b_data = monthly[monthly['B2B'] == 'B2B']
b2c_data = monthly[monthly['B2B'] == 'B2C']

# Dual-axis grouped bar (same as notebook's final chart)
b2b_monthly_fig = go.Figure()
b2b_monthly_fig.add_trace(go.Bar(
    x=b2b_data['month'].astype(str),
    y=b2b_data['total_revenue'],
    name='B2B', marker_color='#FF9900', yaxis='y',
    hovertemplate="B2B %{x}: €%{y:,.0f}<extra></extra>",
))
b2b_monthly_fig.add_trace(go.Bar(
    x=b2c_data['month'].astype(str),
    y=b2c_data['total_revenue'],
    name='B2C', marker_color='#545B64', yaxis='y2',
    hovertemplate="B2C %{x}: €%{y:,.0f}<extra></extra>",
))
b2b_monthly_fig.update_layout(
    template=CHART_TEMPLATE, barmode='group',
    margin=dict(l=8, r=8, t=20, b=8), font=CHART_FONT,
    plot_bgcolor="#fff", paper_bgcolor="#fff",
    yaxis=dict(
        title=dict(text='B2B Revenue (€)', font=dict(color='#FF9900')),
        tickfont=dict(color='#FF9900'),
        showgrid=True,
    ),
    yaxis2=dict(
        title=dict(text='B2C Revenue (€)', font=dict(color='#545B64')),
        tickfont=dict(color='#545B64'),
        overlaying='y', side='right',
        showgrid=False,
    ),
    legend=dict(orientation='h', x=0, y=1.08, font=dict(size=12)),
    xaxis_title="",
)

# AOV comparison B2B vs B2C
customer_summary = df.groupby('B2B').agg(
    total_revenue=('revenue', 'sum'),
    avg_order_value=('revenue', 'mean'),
    order_count=('order_id', 'count'),
).reset_index()
customer_summary['B2B'] = customer_summary['B2B'].replace({True: 'B2B', False: 'B2C'})

b2b_row = customer_summary[customer_summary['B2B'] == 'B2B'].iloc[0]
b2c_row = customer_summary[customer_summary['B2B'] == 'B2C'].iloc[0]


# ── Layout ───────────────────────────────────────────────────────
layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H4(
                [html.I(className="fas fa-users me-2", style={"color": "#FF9900"}),
                 "Customer Analytics"],
                className="mb-1",
                style={"color": "#232F3E", "fontWeight": "700", "fontSize": "20px"},
            ),
            html.P(
                "Cancellations, returns & customer segment analysis · Amazon India Q2 2022",
                className="mb-0", style={"color": "#545B64", "fontSize": "13px"},
            ),
        ]),
    ], className="mb-4"),

    # ── KPI cards ────────────────────────────────────────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.I(className="fas fa-shopping-cart card-icon"),
            html.Div("Total Orders", className="card-title"),
            html.Div(f"{total_orders:,}", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-ban card-icon", style={"color": "#FF9900"}),
            html.Div("Cancelled", className="card-title"),
            html.Div([
                f"{len(cancelled):,}",
                html.Span(f" ({cancel_pct:.1f}%)",
                          style={"fontSize": "14px", "color": "#545B64", "fontWeight": "400"}),
            ], className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-undo card-icon", style={"color": "#232F3E"}),
            html.Div("Returned", className="card-title"),
            html.Div([
                f"{len(returned):,}",
                html.Span(f" ({return_pct:.1f}%)",
                          style={"fontSize": "14px", "color": "#545B64", "fontWeight": "400"}),
            ], className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-building card-icon"),
            html.Div("B2B Orders", className="card-title"),
            html.Div([
                f"{int(b2b_row['order_count']):,}",
                html.Span(f" ({b2b_row['order_count']/total_orders*100:.1f}%)",
                          style={"fontSize": "14px", "color": "#545B64", "fontWeight": "400"}),
            ], className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-receipt card-icon"),
            html.Div("B2B vs B2C AOV", className="card-title"),
            html.Div([
                f"€{b2b_row['avg_order_value']:.2f}",
                html.Span(" / ", style={"color": "#545B64", "fontWeight": "400"}),
                f"€{b2c_row['avg_order_value']:.2f}",
            ], className="card-value", style={"fontSize": "18px"}),
        ], className="card card-body metric-card"), md=True, xs=12),
    ], className="mb-4 g-3"),

    # ── Charts row 1: Donut + Cancellation by category ────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("Order Health Overview", className="chart-card-title"),
            dcc.Graph(figure=donut_fig, config={"displayModeBar": False},
                      style={"height": "340px"}),
        ], className="chart-card"), width=5),

        dbc.Col(html.Div([
            html.Div("Cancellation Rate by Category", className="chart-card-title"),
            html.P("Categories with > 500 orders",
                   style={"fontSize": "11px", "color": "#9AA5AE",
                          "margin": "0 0 4px 0"}),
            dcc.Graph(figure=cancel_cat_fig, config={"displayModeBar": False},
                      style={"height": "320px"}),
        ], className="chart-card"), width=7),
    ], className="mb-4 g-3"),

    # ── Charts row 2: B2B vs B2C monthly ─────────────────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("B2B vs B2C Revenue by Month", className="chart-card-title"),
            html.P(
                "Dual axis — B2B revenue is much smaller in absolute terms.",
                style={"fontSize": "11px", "color": "#9AA5AE", "margin": "0 0 4px 0"},
            ),
            dcc.Graph(figure=b2b_monthly_fig, config={"displayModeBar": False}),
        ], className="chart-card"), width=8),

        dbc.Col(html.Div([
            html.Div("Customer Segment Comparison", className="chart-card-title"),
            dbc.Table.from_dataframe(
                pd.DataFrame({
                    "Metric": ["Orders", "Total Revenue", "Avg Order Value"],
                    "B2B": [
                        f"{int(b2b_row['order_count']):,}",
                        f"€{b2b_row['total_revenue']:,.0f}",
                        f"€{b2b_row['avg_order_value']:.2f}",
                    ],
                    "B2C": [
                        f"{int(b2c_row['order_count']):,}",
                        f"€{b2c_row['total_revenue']:,.0f}",
                        f"€{b2c_row['avg_order_value']:.2f}",
                    ],
                }),
                striped=True, bordered=False, hover=True, className="mb-0",
            ),
            html.P(
                "B2B is ~0.7% of revenue but orders at ~6% higher AOV. "
                "High opportunity if volumes can be grown.",
                className="mt-3 mb-0",
                style={"fontSize": "12px", "color": "#545B64", "lineHeight": "1.6"},
            ),
        ], className="chart-card"), width=4),
    ], className="g-3 mb-4"),

], fluid=True)
