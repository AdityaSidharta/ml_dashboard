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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def get_graph():
    gapminder = px.data.gapminder()
    gapminder_2007 = gapminder.query('year == 2007')
    graph = dcc.Graph(
        id='example-graph-{}'.format(random.getrandbits(64)),
        figure=px.scatter(gapminder_2007, x='gdpPercap', y='lifeExp', template='plotly_dark'),
    )
    return graph

def get_navbar():
    logo = dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px"))
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://plot.ly",
            )
        ]
    )

    # this is the default navbar style created by the NavbarSimple component
    navbar = dbc.NavbarSimple(
        children=[dbc.NavItem(dbc.NavLink("Prediction", href="#")),
                  dbc.NavItem(dbc.NavLink("Groundtruth", href="#")),
                                          logo],
        brand="Machine Learning Dashboard",
        brand_href="#",
        sticky="top",
        className="mb-5",
        color="dark",
        dark=True,
    )

    return navbar

def get_row(n):
    children = []
    for idx in range(n):
        children.append(dbc.Col([html.H2("Graph"), html.Div(get_graph())]))
    row = dbc.Row(children=children, no_gutters=False)
    return row

def get_body(ns):
    children = []
    for n in ns:
        children.append(get_row(n))
    return dbc.Container(children=children)

def create_app(metadata):
    app = dash.Dash(__name__, assets_folder='/home/adityasidharta/git/ml_dashboard/assets', external_stylesheets=[dbc.themes.GRID])
    layouts = [get_navbar(), get_body([1,2,3])]
    app.layout = html.Div(
        layouts,
        style={'backgroundColor': '#33313b'}
    )
    return app


if __name__ == '__main__':
    app = create_app(None)
    app.run_server(debug=True, port = 8090)