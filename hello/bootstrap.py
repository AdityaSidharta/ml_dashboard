import dash_bootstrap_components as dbc
import dash_html_components as html

from hello.dashboard import PLOTLY_LOGO


def navbar():
    logo = dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", className="logo"))],
                    align="center",
                    no_gutters=True,
                ),
                href="https://adityasidharta.com",
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
