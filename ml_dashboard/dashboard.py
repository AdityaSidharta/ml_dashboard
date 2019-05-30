import plotly
import plotly_express as px
from plotly import graph_objs as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import random

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


def get_navbar():
    logo = dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row([dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px"))], align="center", no_gutters=True),
                href="https://plot.ly",
            )
        ]
    )

    # this is the default navbar style created by the NavbarSimple component
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Prediction", href="#")),
            dbc.NavItem(dbc.NavLink("Groundtruth", href="#")),
            logo,
        ],
        brand="Machine Learning Dashboard",
        brand_href="#",
        sticky="top",
        className="mb-5",
        color="dark",
        dark=True,
    )

    return navbar


def get_body(ns):
    children = []
    for n in ns:
        children.append(get_row(n))
    return dbc.Container(children=children)


def get_row(n):
    children = []
    for idx in range(n):
        children.append(
            dbc.Col(
                [
                    html.Div(
                        [
                            html.H4(
                                "hello".upper(),
                                style={
                                    "font-size": "normal",
                                    "font-family": "Helvetica",
                                    "color": "black",
                                    "text-align": "center",
                                    "vertical-align": "center",
                                },
                            ),
                            get_graph(),
                        ],
                        style={"backgroundColor": "white"},
                    )
                ],
                style={"margin-top": 4, "margin-left": 4, "margin-right": 4, "margin-bottom": 4},
            )
        )
    row = dbc.Row(children=children, no_gutters=True)
    return row


def get_graph():
    graph = dcc.Graph(
        id="example-graph-{}".format(random.getrandbits(234)),
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Montréal"},
            ],
            "layout": go.Layout(height=250, margin=dict(l=50, r=50, t=50, b=50)),
        },
    )
    return graph


def create_app(metadata):
    app = dash.Dash(
        __name__, assets_folder="/home/aditya/extrahd/ml_dashboard/ml_dashboard/assets", external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    layouts = [get_navbar(), get_body([1, 2, 3])]
    app.layout = html.Div(layouts, style={"backgroundColor": "#white"})
    return app


if __name__ == "__main__":
    app = create_app(None)
    app.run_server(debug=True, port=8090)
