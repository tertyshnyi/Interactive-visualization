import ast
import folium
from folium.plugins import MarkerCluster
from dash.dependencies import Input, Output, State
from dash import html


def callback_(dash_app, articles_data, authors_locations_data):
    def clean_authors(authors):
        authors = authors.replace("'", "").split(", ")
        return [author.strip() for author in authors]

    articles_data['Authors'] = articles_data['Authors'].apply(ast.literal_eval)
    articles_data['Keywords'] = articles_data['Keywords'].apply(ast.literal_eval)

    authors_locations_data['Authors'] = authors_locations_data['Authors'].fillna('').apply(clean_authors)
    authors_locations_data['Coordinates'] = authors_locations_data['Coordinates'].fillna('').apply(
        lambda x: ast.literal_eval(x) if x != '' else [])

    @dash_app.callback(
        Output('map-container', 'children'),
        [Input('generate-map-button', 'n_clicks')],
        [State('keywords-dropdown', 'value')]
    )
    def update_map(n_clicks, keywords):
        if n_clicks and keywords:
            m = folium.Map(location=[0, 0], zoom_start=2)
            marker_cluster = MarkerCluster().add_to(m)

            filtered_data = articles_data[
                articles_data['Keywords'].apply(lambda x: any(keyword in x for keyword in keywords))]

            authors = filtered_data['Authors'].explode().unique()

            filtered_authors_locations_data = authors_locations_data[
                authors_locations_data['Authors'].apply(lambda x: any(author in x for author in authors))]

            for _, row in filtered_authors_locations_data.iterrows():
                locations = row['Coordinates']
                affiliations = row['Affiliation'].split("', ")
                authors = row['Authors']

                for loc, affiliation, author in zip(locations, affiliations, authors):
                    if isinstance(loc[0], (int, float)) and isinstance(loc[1], (int, float)):
                        author = author.replace(r"\xa0&\xa0", ', ').replace(r"\xa0", " ")
                        affiliation = affiliation.replace(r"'", '')

                        html1 = """<!doctype html>
                                    <head>
                                        <style>
                                            h4 {
                                                text-align: center;
                                            }
                                            h5 {
                                                text-align: left;
                                            }
                                            p {
                                                font-size: 11pt;
                                                text-align: left;
                                            }
                                        </style>
                                    </head>
                                    <body>
                                        <h4>Information about this affiliation</h4>
                                        <hr>
                                        <h5>Title: """ + row['Title'] + """</h5>
                                        <h5>Affiliation: """ + affiliation + """</h5>
                                        <h5>Authors: """ + author + """</h5>
                                    </body>
                                """

                        iframe = folium.IFrame(html=html1, width=250, height=300)
                        popup = folium.Popup(iframe, max_width=2650)

                        lat, lon = loc

                        folium.Marker(location=[lat, lon], radius=5, color='blue',
                                      fill=True, fill_color='blue', fill_opacity=0.2,
                                      popup=popup, tooltip='Click for more info').add_to(marker_cluster)

            map_html = m.get_root().render()

            return html.Iframe(srcDoc=map_html, width='100%', height='600px')

        return html.Div()
