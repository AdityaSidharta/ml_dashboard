import plotly
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def get_navbar():
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("ML Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                )
            )
        ],
        color="dark",
        dark=True,
    )
    return navbar


def create_app(metadata):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div(
        get_navbar(),
        dbc.Row(dbc.Col())
    )
    return app


if __name__ == '__main__':
    app = create_app(None)
    app.run_server(debug=True, port = 8090)