import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path="/sales_overview",
    name="Sales Overview",
)

# ── Chart styling constants ──────────────────────────────────────
AMAZON_COLORS = ["#FF9900", "#146EB4", "#232F3E", "#67B346", "#E47911", "#5C4B8A"]
CHART_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Inter, sans-serif", size=12, color="#545B64")
CHART_MARGIN = dict(l=8, r=8, t=12, b=8)

# ── Data loading ─────────────────────────────────────────────────
df = pd.read_csv("data/Amazon-cleaned.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M').astype(str)

state_options = sorted(df['ship_state'].dropna().unique())
default_state = "KARNATAKA"  # one of the largest markets, good demo state


# ── Layout ───────────────────────────────────────────────────────
layout = dbc.Container([

    # ── Page header ──────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            html.H4(
                [html.I(className="fas fa-chart-line me-2", style={"color": "#FF9900"}),
                 "Sales Overview"],
                className="mb-1",
                style={"color": "#232F3E", "fontWeight": "700", "fontSize": "20px"},
            ),
            html.P("State-level performance analytics · Amazon India Q2 2022",
                   className="mb-0", style={"color": "#545B64", "fontSize": "13px"}),
        ]),
    ], className="mb-3"),

    # ── Filter bar ───────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.InputGroupText(
                    [html.I(className="fas fa-map-marker-alt me-1"), " State"],
                    style={"backgroundColor": "#F2F3F3", "color": "#545B64",
                           "fontSize": "13px", "border": "1px solid #D5D9D9"},
                ),
                html.Div(
                    dcc.Dropdown(
                        id="state-dropdown",
                        options=[{"label": s.title(), "value": s} for s in state_options],
                        value=default_state,
                        placeholder="Select a state…",
                        clearable=False,
                        searchable=True,
                        style={"fontSize": "14px", "minWidth": "240px",
                               "border": "none", "borderLeft": "none"},
                    ),
                    style={"flex": "1", "zIndex": 9999, "position": "relative"},
                ),
            ], style={"maxWidth": "420px"}),
        ]),
    ], className="mb-4"),

    # ── KPI metric cards ─────────────────────────────────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.I(className="fas fa-shopping-cart card-icon"),
            html.Div("Total Orders", className="card-title"),
            html.Div(id="metric-orders", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-euro-sign card-icon"),
            html.Div("Total Revenue", className="card-title"),
            html.Div(id="metric-revenue", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-receipt card-icon"),
            html.Div("Avg Order Value", className="card-title"),
            html.Div(id="metric-aov", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-building card-icon"),
            html.Div("B2B Share", className="card-title"),
            html.Div(id="metric-b2b", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-star card-icon"),
            html.Div("Top Category", className="card-title"),
            html.Div(id="metric-top-cat", className="card-value",
                     style={"fontSize": "15px", "lineHeight": "1.3"}),
        ], className="card card-body metric-card"), md=True, xs=12),
    ], className="mb-4 g-3"),

    # ── Charts row 1: Categories + Monthly Revenue ────────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("Top Product Categories", className="chart-card-title"),
            dcc.Graph(id="top-categories", config={"displayModeBar": False}),
        ], className="chart-card"), width=6),

        dbc.Col(html.Div([
            html.Div("Monthly Revenue Trend", className="chart-card-title"),
            dcc.Graph(id="monthly-revenue", config={"displayModeBar": False}),
        ], className="chart-card"), width=6),
    ], className="mb-4 g-3"),

    # ── Charts row 2: Order Status + Cancellations ────────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("Order Status Distribution", className="chart-card-title"),
            dcc.Graph(id="order-status", config={"displayModeBar": False}),
        ], className="chart-card"), width=6),

        dbc.Col(html.Div([
            html.Div("Cancellations & Returns", className="chart-card-title"),
            dcc.Graph(id="cancellations-chart", config={"displayModeBar": False}),
        ], className="chart-card"), width=6),
    ], className="mb-4 g-3"),

    # ── Charts row 3: B2B vs B2C + Summary table ─────────────────
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("B2B vs B2C Revenue by Month", className="chart-card-title"),
            dcc.Graph(id="b2b-chart", config={"displayModeBar": False}),
        ], className="chart-card"), width=6),

        dbc.Col(html.Div([
            html.Div("Summary Metrics", className="chart-card-title"),
            html.Div(id="summary-metrics"),
        ], className="chart-card"), width=6),
    ], className="g-3 mb-4"),

], fluid=True)


# ── Callback ─────────────────────────────────────────────────────
@callback(
    Output("top-categories", "figure"),
    Output("monthly-revenue", "figure"),
    Output("order-status", "figure"),
    Output("cancellations-chart", "figure"),
    Output("b2b-chart", "figure"),
    Output("summary-metrics", "children"),
    Output("metric-orders", "children"),
    Output("metric-revenue", "children"),
    Output("metric-aov", "children"),
    Output("metric-b2b", "children"),
    Output("metric-top-cat", "children"),
    Input("state-dropdown", "value"),
)
def update_dashboard(state):
    empty = go.Figure().update_layout(
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        xaxis={"visible": False}, yaxis={"visible": False},
        annotations=[{"text": "No data", "showarrow": False,
                       "font": {"size": 14, "color": "#545B64"}}]
    )
    no_data = ("—", "—", "—", "—", "—")

    if not state:
        return empty, empty, empty, empty, empty, html.Div("Please select a state."), *no_data

    subset = df[df['ship_state'].str.upper() == state.upper()]
    if subset.empty:
        return empty, empty, empty, empty, empty, html.Div("No data for selected state."), *no_data

    # ── Top Categories ───────────────────────────────────────────
    top_cats = subset.groupby('category')['qty'].sum().nlargest(6).reset_index()
    cat_fig = px.bar(
        top_cats, x='category', y='qty',
        color='category', color_discrete_sequence=AMAZON_COLORS,
        template=CHART_TEMPLATE,
    )
    cat_fig.update_layout(
        showlegend=False, margin=CHART_MARGIN, font=CHART_FONT,
        xaxis_title="", yaxis_title="Units Sold",
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        xaxis=dict(tickfont=dict(size=11)),
    )
    cat_fig.update_traces(marker_line_width=0)

    # ── Monthly Revenue ──────────────────────────────────────────
    monthly = subset.groupby('month')['amount_eu'].sum().reset_index()
    rev_fig = px.line(
        monthly, x='month', y='amount_eu',
        markers=True, template=CHART_TEMPLATE,
        color_discrete_sequence=["#FF9900"],
    )
    rev_fig.update_traces(line=dict(width=2.5), marker=dict(size=6, color="#FF9900"))
    rev_fig.update_layout(
        margin=CHART_MARGIN, font=CHART_FONT,
        xaxis_title="", yaxis_title="Revenue (€)",
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        xaxis=dict(tickangle=-30, tickfont=dict(size=10)),
    )

    # ── Order Status ─────────────────────────────────────────────
    top_status = subset['status'].value_counts().nlargest(5).reset_index()
    top_status.columns = ['status', 'count']
    status_fig = px.bar(
        top_status, x='count', y='status', orientation='h',
        color='status', color_discrete_sequence=AMAZON_COLORS,
        template=CHART_TEMPLATE,
    )
    status_fig.update_layout(
        showlegend=False, margin=CHART_MARGIN, font=CHART_FONT,
        xaxis_title="Orders", yaxis_title="",
        plot_bgcolor="#fff", paper_bgcolor="#fff",
    )
    status_fig.update_traces(marker_line_width=0)

    # ── Cancellations & Returns ──────────────────────────────────
    cancelled = subset[subset['status'] == 'Cancelled']
    returned  = subset[subset['status'] == 'Shipped - Returned to Seller']
    delivered = subset[~subset['status'].isin(['Cancelled', 'Shipped - Returned to Seller'])]

    cancel_fig = go.Figure(data=[go.Pie(
        labels=['Delivered / Active', 'Cancelled', 'Returned'],
        values=[len(delivered), len(cancelled), len(returned)],
        hole=0.55,
        marker_colors=['#67B346', '#FF9900', '#232F3E'],
        textinfo='percent+label',
        textfont=dict(size=11, family="Inter, sans-serif"),
        hovertemplate="%{label}: %{value:,} orders (%{percent})<extra></extra>",
    )])
    cancel_fig.update_layout(
        margin=dict(l=8, r=8, t=20, b=8), font=CHART_FONT,
        paper_bgcolor="#fff", showlegend=False,
        annotations=[dict(
            text=f"{len(subset):,}<br><span style='font-size:11px;color:#545B64'>orders</span>",
            x=0.5, y=0.5, font=dict(size=16, color="#232F3E"), showarrow=False
        )],
    )

    # ── B2B vs B2C by Month ──────────────────────────────────────
    month_order = ['2022-04', '2022-05', '2022-06']
    month_labels = {'2022-04': 'April', '2022-05': 'May', '2022-06': 'June'}

    b2b_monthly = (
        subset.groupby(['month', 'B2B'])['amount_eu']
        .sum().reset_index()
    )
    b2b_monthly['B2B'] = b2b_monthly['B2B'].replace({True: 'B2B', False: 'B2C'})
    b2b_monthly = b2b_monthly[b2b_monthly['month'].isin(month_order)].copy()
    b2b_monthly['month_label'] = b2b_monthly['month'].map(month_labels)

    b2b_data  = b2b_monthly[b2b_monthly['B2B'] == 'B2B']
    b2c_data  = b2b_monthly[b2b_monthly['B2B'] == 'B2C']

    b2b_fig = go.Figure()
    b2b_fig.add_trace(go.Bar(
        x=b2b_data['month_label'], y=b2b_data['amount_eu'],
        name='B2B', marker_color='#FF9900', yaxis='y',
        hovertemplate="B2B %{x}: €%{y:,.0f}<extra></extra>",
    ))
    b2b_fig.add_trace(go.Bar(
        x=b2c_data['month_label'], y=b2c_data['amount_eu'],
        name='B2C', marker_color='#232F3E', yaxis='y2',
        hovertemplate="B2C %{x}: €%{y:,.0f}<extra></extra>",
    ))
    b2b_fig.update_layout(
        template=CHART_TEMPLATE, barmode='group',
        margin=CHART_MARGIN, font=CHART_FONT,
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        yaxis=dict(title=dict(text='B2B Revenue (€)', font=dict(color='#FF9900')),
                   tickfont=dict(color='#FF9900'), showgrid=True),
        yaxis2=dict(title=dict(text='B2C Revenue (€)', font=dict(color='#545B64')),
                    tickfont=dict(color='#545B64'), overlaying='y', side='right',
                    showgrid=False),
        legend=dict(orientation='h', x=0, y=1.08, font=dict(size=11)),
        xaxis_title="",
    )

    # ── Summary Metrics ──────────────────────────────────────────
    total_orders    = len(subset)
    total_revenue   = subset['amount_eu'].sum()
    avg_order_value = subset['amount_eu'].mean()
    b2b_share       = subset['B2B'].mean() * 100
    top_category    = top_cats.iloc[0]['category'] if not top_cats.empty else "N/A"

    table = dbc.Table.from_dataframe(
        pd.DataFrame({
            "Metric": ["Total Orders", "Total Revenue", "Average Order Value",
                       "B2B Share (%)", "Top Category"],
            "Value": [
                f"{total_orders:,}",
                f"€{total_revenue:,.0f}",
                f"€{avg_order_value:,.0f}",
                f"{b2b_share:.1f}%",
                top_category,
            ],
        }),
        striped=True, bordered=False, hover=True, className="mb-0",
    )

    return (
        cat_fig, rev_fig, status_fig, cancel_fig, b2b_fig, table,
        f"{total_orders:,}",
        f"€{total_revenue:,.0f}",
        f"€{avg_order_value:,.0f}",
        f"{b2b_share:.1f}%",
        top_category,
    )
