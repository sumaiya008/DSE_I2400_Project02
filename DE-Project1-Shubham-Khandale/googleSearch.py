from googlesearch import search
from DbOps import DbOps
import urllib.request
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

databaseName = 'my_custom_bot'
tablename = 'scrapedData'

searchEngines = {'google': 'http://google.com/search?q=',
                 '1': 'http://google.com/search?q=',
                 'bing': 'https://www.bing.com/search?q=',
                 '2': 'https://www.bing.com/search?q=',
                 'Yahoo': 'https://search.yahoo.com/search?p=',
                 '3': 'https://search.yahoo.com/search?p=',
                 'DuckDuckGo': 'https://html.duckduckgo.com/html/?q=',
                 '4': 'https://html.duckduckgo.com/html/?q='
                 }

DBobejct = DbOps(databaseName, tablename)
DBobejct.connect()


def googleSearch(keyword, searchengine):
    # tabUrl = "http://google.com/search?q="

    allTitles = []

    try:
        urls = list(set(search(searchEngines.get(str(searchengine.lower()), None) + keyword)))
        print(urls)

        if not urls == None:
            for i in tqdm(range(len(urls))):
                try:

                    # Make a request to the webpage
                    # response = requests.get(urls[i])
                    response = urllib.request.urlopen(urls[i])

                    # Parse the HTML content using Beautiful Soup
                    soup = BeautifulSoup(response.read(), 'html.parser')

                except:
                    print("Authorization Failed \n")

                # Find the data you want using Beautiful Soup methods
                try:
                    title = soup.title.text.strip()
                    try:
                        heading = soup.h1.text.strip()
                    except:
                        heading = 'Null'

                    paragraphs = " "
                    for p in soup.find_all([ 'h2', 'p']):
                        paragraphs += re.sub('\W+', ' ', p.text.strip())
                        paragraphs += " "
                        # paragraphs = [p.text.strip() for p in soup.find_all('p')]

                    # Print the data
                    print('Title:', title)
                    print('Heading:', heading)
                    # print("*" * 100)
                    print('Paragraphs:', paragraphs[:1000])
                    print("\n")

                    # Checking if the data contains any ads sponsored
                    pattern = r'\b(ad|ads|advertisement|sponsor(ed)?)\b'
                    if re.search(pattern, paragraphs[:1000]):
                        print("The string contains ads or advertising data.")
                        break

                    if title not in allTitles:
                        allTitles.append(title)
                        DBobejct.insertQuery(searchengine,keyword, urls[i], title, heading, paragraphs[:1000])

                    else:
                        print("already title exists")
                except:
                    print("An exception occurred")

    except:
        print("Enter Correct Name")
