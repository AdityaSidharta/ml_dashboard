from plotly import graph_objs as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import random

from hello.metadata import Metadata
from hello.bootstrap import navbar

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


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


def get_card(
    prediction_df,
    prediction_key,
    prediction_timestamp,
    prediction_value,
    name,
    col,
    plot_type,
    grouper,
    granularity,
    aggregation,
):
    card = dbc.Card([dbc.CardHeader(name), dbc.CardBody([get_graph()])], color="success")
    container = dbc.Container(dbc.Row(dbc.Col(card)))
    return container


def create_app(metadata):
    app = dash.Dash(
        __name__,
        assets_folder="/home/aditya/extrahd/ml_dashboard/ml_dashboard/assets",
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    layouts = []
    layouts.append(navbar())
    for idx, prediction_card in enumerate(metadata.prediction_cards):
        name = prediction_card["name"]
        col = prediction_card["col"]
        plot_type = prediction_card["plot_type"]
        grouper = prediction_card["grouper"]
        granularity = prediction_card["granularity"]
        aggregation = prediction_card["aggregation"]
        layouts.append(
            get_card(
                metadata.prediction_df,
                metadata.prediction_key,
                metadata.prediction_timestamp,
                metadata.prediction_value,
                name,
                col,
                plot_type,
                grouper,
                granularity,
                aggregation,
            )
        )
    app.layout = html.Div(layouts, style={"backgroundColor": "#white"}, className="app")
    return app


if __name__ == "__main__":
    meta = Metadata()
    meta.load_config('/home/aditya/extrahd/ml_dashboard/example/config_example.yml')
    app = create_app(meta)
    app.run_server(debug=True, port=8090)
