import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path="/dwdwa",
    name="Product Analytics",
)

# ── Chart styling constants ──────────────────────────────────────
AMAZON_COLORS = ["#FF9900", "#146EB4", "#232F3E", "#67B346", "#E47911", "#5C4B8A"]
CHART_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Inter, sans-serif", size=12, color="#545B64")

# ── Data (precomputed — no interactive filter on this page) ──────
df = pd.read_csv("data/Amazon-cleaned.csv")
df['revenue'] = df['amount_eu']

# ── Category Revenue % ───────────────────────────────────────────
category_revenue = (
    df.groupby('category')[['revenue']].sum()
    .pipe(lambda x: x / x.sum() * 100)
    .sort_values('revenue', ascending=True)
    .reset_index()
)
category_revenue.columns = ['category', 'pct_revenue']

cat_rev_fig = px.bar(
    category_revenue, x='pct_revenue', y='category', orientation='h',
    color='pct_revenue',
    color_continuous_scale=[[0, '#FFE0A8'], [1, '#E47911']],
    template=CHART_TEMPLATE,
    custom_data=['category'],
)
cat_rev_fig.update_traces(
    marker_line_width=0,
    hovertemplate="<b>%{customdata[0]}</b><br>%{x:.1f}% of revenue<extra></extra>",
)
cat_rev_fig.update_layout(
    margin=dict(l=8, r=8, t=12, b=8), font=CHART_FONT,
    xaxis_title="% of Total Revenue", yaxis_title="",
    plot_bgcolor="#fff", paper_bgcolor="#fff",
    showlegend=False, coloraxis_showscale=False,
    xaxis=dict(range=[0, category_revenue['pct_revenue'].max() * 1.15]),
)

# Add value labels on bars
for _, row in category_revenue.iterrows():
    cat_rev_fig.add_annotation(
        x=row['pct_revenue'] + 0.5,
        y=row['category'],
        text=f"{row['pct_revenue']:.1f}%",
        showarrow=False,
        font=dict(size=11, color="#232F3E"),
        xanchor='left',
    )

# ── Product Portfolio Matrix ─────────────────────────────────────
category_metrics = df.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    avg_order_value=('revenue', 'mean'),
).reset_index()
category_metrics['revenue_10k'] = category_metrics['total_revenue'] / 10000

median_rev = category_metrics['revenue_10k'].median()
median_aov = category_metrics['avg_order_value'].median()

portfolio_fig = go.Figure()

# Scatter points
for _, row in category_metrics.iterrows():
    portfolio_fig.add_trace(go.Scatter(
        x=[row['revenue_10k']],
        y=[row['avg_order_value']],
        mode='markers+text',
        marker=dict(
            size=max(12, min(40, row['total_revenue'] / 8000)),
            color='#FF9900',
            opacity=0.8,
            line=dict(color='#E47911', width=1.5),
        ),
        text=[row['category']],
        textposition='top right',
        textfont=dict(size=11, color='#232F3E'),
        name=row['category'],
        hovertemplate=(
            f"<b>{row['category']}</b><br>"
            f"Revenue: €{row['total_revenue']:,.0f}<br>"
            f"Avg Order: €{row['avg_order_value']:.2f}<extra></extra>"
        ),
        showlegend=False,
    ))

# Quadrant lines
portfolio_fig.add_hline(y=median_aov, line_dash='dot', line_color='#C8CDD0', line_width=1.5)
portfolio_fig.add_vline(x=median_rev, line_dash='dot', line_color='#C8CDD0', line_width=1.5)

# Quadrant labels
quadrant_style = dict(showarrow=False, font=dict(size=10, color='#9AA5AE'),
                      bgcolor='rgba(255,255,255,0.7)', borderpad=3)
portfolio_fig.add_annotation(x=median_rev * 0.1, y=median_aov * 1.55,
    text="Niche Upside", **quadrant_style)
portfolio_fig.add_annotation(x=median_rev * 5, y=median_aov * 1.55,
    text="Premium Performers ⭐", **quadrant_style)
portfolio_fig.add_annotation(x=median_rev * 0.1, y=median_aov * 0.45,
    text="Underperformers", **quadrant_style)
portfolio_fig.add_annotation(x=median_rev * 5, y=median_aov * 0.45,
    text="Volume Drivers", **quadrant_style)

portfolio_fig.update_layout(
    template=CHART_TEMPLATE,
    margin=dict(l=8, r=8, t=20, b=8), font=CHART_FONT,
    xaxis_title="Total Revenue (€10k)", yaxis_title="Avg Order Value (€)",
    plot_bgcolor="#fff", paper_bgcolor="#fff",
)

# ── KPI cards (global totals) ────────────────────────────────────
total_rev = df['revenue'].sum()
top_cat   = category_revenue.sort_values('pct_revenue', ascending=False).iloc[0]
n_cats    = df['category'].nunique()
avg_aov   = df['revenue'].mean()


# ── Layout ───────────────────────────────────────────────────────
layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            html.H4(
                [html.I(className="fas fa-trophy me-2", style={"color": "#FF9900"}),
                 "Product Analytics"],
                className="mb-1",
                style={"color": "#232F3E", "fontWeight": "700", "fontSize": "20px"},
            ),
            html.P("Revenue share, portfolio positioning · Amazon India Q2 2022",
                   className="mb-0", style={"color": "#545B64", "fontSize": "13px"}),
        ]),
    ], className="mb-4"),

    # KPI cards
    dbc.Row([
        dbc.Col(html.Div([
            html.I(className="fas fa-euro-sign card-icon"),
            html.Div("Total Revenue", className="card-title"),
            html.Div(f"€{total_rev:,.0f}", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-tags card-icon"),
            html.Div("Product Categories", className="card-title"),
            html.Div(str(n_cats), className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-crown card-icon"),
            html.Div("Top Category", className="card-title"),
            html.Div(top_cat['category'], className="card-value",
                     style={"fontSize": "16px"}),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-chart-pie card-icon"),
            html.Div("Top Category Share", className="card-title"),
            html.Div(f"{top_cat['pct_revenue']:.1f}%", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=6),

        dbc.Col(html.Div([
            html.I(className="fas fa-receipt card-icon"),
            html.Div("Avg Order Value", className="card-title"),
            html.Div(f"€{avg_aov:.2f}", className="card-value"),
        ], className="card card-body metric-card"), md=True, xs=12),
    ], className="mb-4 g-3"),

    # Charts
    dbc.Row([
        dbc.Col(html.Div([
            html.Div("Revenue Share by Category", className="chart-card-title"),
            dcc.Graph(figure=cat_rev_fig, config={"displayModeBar": False},
                      style={"height": "360px"}),
        ], className="chart-card"), width=5),

        dbc.Col(html.Div([
            html.Div(
                "Product Portfolio Matrix · Revenue vs. Average Order Value",
                className="chart-card-title",
            ),
            html.P(
                "Bubble size = total revenue. Quadrants split at median values.",
                style={"fontSize": "11px", "color": "#9AA5AE", "margin": "0 0 4px 0"},
            ),
            dcc.Graph(figure=portfolio_fig, config={"displayModeBar": False},
                      style={"height": "340px"}),
        ], className="chart-card"), width=7),
    ], className="mb-4 g-3"),

], fluid=True)
