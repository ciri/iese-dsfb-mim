import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

app = Dash(
    __name__,
    use_pages=True,
    title="Amazon Seller Analytics",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

sidebar = html.Div(
    [
        # Logo
        html.Div(
            html.Img(src="assets/logos/amazon.svg", style={"height": "32px"}),
            className="sidebar-logo",
        ),
        # Nav section label
        html.Div("Navigation", className="sidebar-section-label"),
        # Nav links
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-chart-line fa-fw me-2"), "Sales Overview"],
                    href="/sales_overview",
                    active="exact",
                ),
                dbc.NavLink(
                    [html.I(className="fas fa-trophy fa-fw me-2"), "Product Analytics"],
                    href="/dwdwa",
                    active="exact",
                ),
                dbc.NavLink(
                    [html.I(className="fas fa-users fa-fw me-2"), "Customer Analytics"],
                    href="/dwdaw",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
        # Footer credits
        html.Div(
            [
                html.Span("Created by "),
                html.A("Enric", href="https://github.com/ciri/dsfb-iese", target="_blank"),
                html.Br(),
                html.Span("Based on work by "),
                html.A("Mayara Daher", href="https://github.com/mayaradaher", target="_blank"),
                html.Br(),
                html.Span("Data: "),
                html.A(
                    "MIT Publication",
                    href="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/YGLYDY",
                    target="_blank",
                ),
            ],
            className="subtitle-sidebar sidebar-footer",
        ),
    ],
    className="sidebar",
)

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="icon" href="/assets/logos/favicon.svg" type="image/svg+xml">
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
"""

app.layout = html.Div(
    [
        dcc.Location(id="url", pathname="/sales_overview"),
        sidebar,
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
