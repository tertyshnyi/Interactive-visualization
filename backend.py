import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import csv
from geopy.geocoders import Nominatim


def get_articles_data():
    page = 1
    articles_data = []
    articles1_data = []

    df1 = pd.read_csv('data/articles.csv')

    while page:
        response = requests.get('https://link.springer.com/search/page/' + str(page) +
                                '?query=&search-within=Journal&facet-journal-id=12369')

        soup = BeautifulSoup(response.content, 'html.parser')

        article_list = soup.find('ol', id='results-list', class_='content-item-list')

        if article_list is not None:
            articles = article_list.find_all('li')

            for article in articles:
                article_link = article.find('a', class_='title')
                if article_link is not None:
                    article_url = article_link.get('href')
                    article_response = requests.get('https://link.springer.com' + article_url)
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')

                    author_list = article_soup.find('ul', {'data-test': 'authors-list'})
                    if author_list is not None:
                        author_names = author_list.find_all('a', {'data-test': 'author-name'})
                        authors = [author.text for author in author_names]
                    else:
                        authors = []

                    affiliations_list = article_soup.find('ol', {'class': 'c-article-author-affiliation__list'})
                    if affiliations_list is not None:
                        affiliations_names = affiliations_list.find_all('p', {'class': 'c-article-author-affiliation__address'})
                        authors_names = affiliations_list.find_all('p', {'class': 'c-article-author-affiliation__authors-list'})
                        affiliations = [affiliation.text for affiliation in affiliations_names]
                        authors1 = [author1.text for author1 in authors_names]
                    else:
                        affiliations = []
                        authors1 = []

                    key_list = article_soup.find('ul', {'class': 'c-article-subject-list'})
                    title = article_link.text.strip()

                    if key_list is not None:
                        keys_list = key_list.find_all('span')
                        keywords = [key.text for key in keys_list]
                        if keys_list:
                            article_data = {'Title': title, 'Authors': authors, 'Keywords': keywords}
                            articles_data.append(article_data)
                    else:
                        article_data = {'Title': title, 'Authors': authors, 'Keywords': ''}
                        articles_data.append(article_data)

                    article1_data = {'Title': title, 'Affiliation': affiliations, 'Authors': authors1}
                    articles1_data.append(article1_data)

        if soup.find('a', {'class': 'next'}) is None:
            break
        else:
            page += 1

    if df1.empty or not df1.equals(pd.DataFrame(articles_data)):
        df1 = pd.DataFrame(articles_data)
        df2 = pd.DataFrame(articles1_data)
        df1.to_csv('data/articles.csv', index=False)
        df2.to_csv('data/authors_locations.csv', index=False)
        print('Articles data saved')
    else:
        print('No new articles data found')


def correct_articles_data():
    with open('data/articles.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = []
        for row in reader:
            row = [cell.replace('[', '').replace(']', '') for cell in row]
            if row[2] not in [None, '']:
                rows.append(row)

    with open('data/correct_articles.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)

    with open('data/authors_locations.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = []
        for row in reader:
            row = [cell.replace('[', '').replace(']', '') for cell in row]
            rows.append(row)

    with open('data/correct_authors_locations.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)


def locations():
    geolocator = Nominatim(user_agent="MyApp")

    df = pd.read_csv('data/correct_authors_locations.csv')
    df['Coordinates'] = None

    for index, row in df.iterrows():
        coordinates = []
        if isinstance(row['Affiliation'], str) and row['Affiliation'].strip() != '':
            for element in row['Affiliation'].split("', "):
                try:
                    location = geolocator.geocode(element)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = ", ".join(elements[0:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", ".join(elements[1:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = ", ".join(elements[1:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", " + elements[1].strip() + ", ".join(elements[2:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[1].strip() + ", ".join(elements[2:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", ".join(elements[2:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = ", ".join(elements[2:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", " + elements[1].strip() + ", " + \
                                          elements[2].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[1].strip() + ", " + elements[2].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", " + elements[2].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", " + elements[1].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[2].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[1].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = ", ".join(elements[3:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 5:
                            new_address = elements[5].strip() + ", " + ", ".join(elements[1:2])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 7:
                            new_address = elements[6].strip() + ", " + elements[7].strip() + ", ".join(elements[3:4])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[0].strip() + ", ".join(elements[6:])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = ", ".join(elements[2:4])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = elements[2].strip() + ", ".join(elements[-4:-1])
                            location = geolocator.geocode(new_address)

                    if location is None:
                        elements = element.split(",")
                        if len(elements) > 1:
                            new_address = ", ".join(elements[-4:-1])
                            location = geolocator.geocode(new_address)

                    if location is not None:
                        coordinates.append((location.latitude, location.longitude))
                    else:
                        coordinates.append(('', ''))

                except:
                    coordinates.append(('', ''))
        else:
            continue

        if coordinates:
            df.at[index, 'Coordinates'] = coordinates

        df.to_csv('data/correct_authors_locations.csv', index=False)
        time.sleep(1)


def time_update():
    while True:
        now = datetime.datetime.now()
        if 2 <= now.hour <= 4:
            get_articles_data()
            correct_articles_data()
            locations()
            time.sleep(3600)
        else:
            print('Data will be update later')
            time.sleep(3600)
