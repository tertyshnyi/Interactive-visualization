from dash import html
import dash_bootstrap_components as dbc


def navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(html.Form([
                    dbc.Button("Journal",
                               id="journal-button", color="link",
                               style={"cursor": "pointer", "text-decoration": "none", "color": "white"})],
                    action="/journal")),
                dbc.NavItem(html.Form([
                    dbc.Button("Sign Out",
                               id="logout-button", color="link",
                               style={"cursor": "pointer", "text-decoration": "none", "color": "white"})],
                    action="/logout", method="post", id="logout-form")),
            ],
            brand="Interactive Map",
            brand_href="/dashboard",
            color="dark",
            dark=True,
        )
    ])
    return layout
