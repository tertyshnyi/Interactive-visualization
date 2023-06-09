from dash import html, dcc
import dash_bootstrap_components as dbc

colors = {
        'background': '#141e30',
        'text': '#000000'
    }


def layout(articles_data):
    unique_keywords = set(keyword for keywords in articles_data['Keywords'] for keyword in keywords)
    return html.Div(children=[
        dbc.Col([
            html.Br(), html.Br(), html.Br(), html.Br(),
            html.H1("Kosice", style={'text-align': 'left', 'color': 'white'}),
            html.H1("Authentic",
                    style={'text-align': 'left', 'margin-top': '-1.5%', 'font-weight': 'bold', 'color': 'white'}),
            html.H5("The home of computer science materials", style={'text-align': 'left', 'color': 'white'})
        ], style={'margin-left': '6.5%', 'color': colors['text']}),

        html.Div(children=[
            html.Br(),
            html.Div(
                style={'width': '250px', 'color': colors['text'], 'margin-left': '6.5%'}, children=[
                    html.Br(),
                    html.Br(),
                    html.Label(
                        'Please select the keywords that interest you to find a publication associated with those'
                        ' keywords and locate the university that published that publication.',
                        style={'textAlign': 'left', 'color': '#FFFFFF', 'fontSize': '16px'}),
                    html.Br(), html.Br(),
                ]),
            html.Div(
                children=[
                    dcc.Dropdown(
                        id='keywords-dropdown',
                        options=[{'label': keyword, 'value': keyword} for keyword in unique_keywords],
                        placeholder='Select the keywords',
                        multi=True,
                        style={
                            'margin-left': '5.5%',
                            'width': '300px',
                            'background-color': 'black',
                            'color': 'white',
                            'border': 'none'
                        }
                    ), html.Br(),
                    html.Button('Generate map',
                                id='generate-map-button',
                                style={"color": "rgb(255, 255, 255)", "font-size": "12px", "width": "14%",
                                       "text-align": "center", 'margin-left': '43%', 'backdrop-filter': 'blur(3px)',
                                       'border': 'none'},
                                hidden=False,
                                ),
                    html.Br(), html.Br(), html.Br(),
                    html.Div(id='map-container', style={"margin": "5%"})
                ]
            ),
        ]),
    ])

