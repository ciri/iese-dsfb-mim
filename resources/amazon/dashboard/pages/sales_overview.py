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

# Load and prepare data
df = pd.read_csv("data/Amazon-cleaned.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M').astype(str)


state_options = sorted(df['ship_state'].dropna().unique())
default_state = state_options[0] if state_options else None

# Layout
layout = dbc.Container([
    html.H2("State Performance Dashboard", className="my-4", style={"color": "#232F3E"}),
    dcc.Dropdown(
        id="state-dropdown",
        options=[{"label": s, "value": s} for s in state_options],
        value=default_state,  # ✅ Select first state automatically
        placeholder="Select a state",
        className="mb-4",
        style={"backgroundColor": "#fff3e0"}
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id="top-categories"), width=6),
        dbc.Col(dcc.Graph(id="monthly-revenue"), width=6),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="order-status"), width=6),
        dbc.Col(html.Div(id="summary-metrics"), width=6),
    ]),
], fluid=True)


@callback(
    Output("top-categories", "figure"),
    Output("monthly-revenue", "figure"),
    Output("order-status", "figure"),
    Output("summary-metrics", "children"),
    Input("state-dropdown", "value"),
)
def update_dashboard(state):
    if not state:
        return go.Figure(), go.Figure(), go.Figure(), html.Div("Please select a state.")

    subset = df[df['ship_state'].str.upper() == state.upper()]
    if subset.empty:
        return go.Figure(), go.Figure(), go.Figure(), html.Div("No data for selected state.")

    # Top Categories
    top_cats = subset.groupby('category')['qty'].sum().nlargest(6).reset_index()
    cat_fig = px.bar(top_cats, x='category', y='qty', title="Top Product Categories", color='category')

    # Monthly Revenue
    monthly = subset.groupby('month')['amount_eu'].sum().reset_index()
    rev_fig = px.line(monthly, x='month', y='amount_eu', title="Monthly Revenue Trend", markers=True)

    # Order Status
    top_status = subset['status'].value_counts().nlargest(5).reset_index()
    top_status.columns = ['status', 'count']
    status_fig = px.bar(top_status, x='count', y='status', orientation='h', title="Top 5 Order Statuses", color='status')

    # Summary Metrics
    total_orders = len(subset)
    total_revenue = subset['amount_eu'].sum()
    avg_order_value = subset['amount_eu'].mean()
    b2b_share = subset['B2B'].mean() * 100
    top_category = top_cats.iloc[0]['category'] if not top_cats.empty else "N/A"

    table = dbc.Table.from_dataframe(pd.DataFrame({
        "Metric": ["Total Orders", "Total Revenue", "Average Order Value", "B2B Share (%)", "Top Category"],
        "Value": [total_orders, f"€{total_revenue:,.0f}", f"€{avg_order_value:,.0f}", f"{b2b_share:.1f}%", top_category]
    }), striped=True, bordered=True, hover=True)

    return cat_fig, rev_fig, status_fig, table
