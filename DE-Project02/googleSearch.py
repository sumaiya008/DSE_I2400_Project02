from googlesearch import search
from DbOps import DbOps
import urllib.request
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os
import requests
from serpapi import GoogleSearch

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



def Search(keyword, searchengine):
    # tabUrl = "http://google.com/search?q="

    if searchengine =='Bing':
        url = f'https://www.bing.com/search?q={keyword}'
        # creating a response object for storing all the information from the url
        resp = requests.get(url)
        # using beautiful soup converting response into a nested data structure
        soup = BeautifulSoup(resp.text, 'html.parser')
        # selecting all the classes which we gonna use to extract info we require
        tags = soup.select('ol#b_results > li.b_algo')

        # creating an empty list to store the results
        results = []

        # iterating over tags
        for i in tags:
            try:
                # selecting url using href tags
                url = (i.select_one('a[href]')).get('href', u'')
                # selecting title using h2 tags
                title = (i.select_one('h2')).text.strip()
                # selecting text using p tags
                if len(((i.select_one('p')).text.strip()).split("·"))>1:
                    text = ((i.select_one('p')).text.strip()).split("·")[1]
                else:
                    text = ((i.select_one('p')).text.strip())

                # append this as a dict into the result
                results.append({'query': keyword,
                                'link': url,
                                'title': title,
                                'text': text})
            except:
                print("Error in fetching data")
                continue

            DBobejct.insertQuery(keyword, searchengine, url, title, text)
        # returing list of dictionaries
        return results


    elif searchengine =='Yahoo':

        # completing the url using user defined query
        url = f'https://search.yahoo.com/search?p={keyword}&ei=UTF-8&nojs=1'
        # creating a response object for storing all the information from the url
        resp = requests.get(url)
        # using beautiful soup converting response into a nested data structure
        soup = BeautifulSoup(resp.text, 'html.parser')
        # selecting all the classes which we gonna use to extract info we require
        tags = soup.select('div#web li div.dd.algo.algo-sr')

        # creating an empty list to store the results
        results = []

        for i in tags:
            try:
                # selecting url using href tags
                link = (i.select_one('div.compTitle h3.title a')).get('href', u'')

                # selecting title using h3_title tags
                if len(((i.select_one('div.compTitle h3.title')).text.strip()).split(" › ")) > 1:
                    title = ((i.select_one('div.compTitle h3.title')).text.strip()).split(" › ")[2]
                    title = re.sub(r'([a-z])([A-Z])', r'\1 \2', title)
                else:
                    title = ((i.select_one('div.compTitle h3.title')).text.strip())
                    title = re.sub(r'([a-z])([A-Z])', r'\1 \2', title)


                # selecting text using comptext tags
                if len(((i.select_one('div.compText')).text.strip()).split("·")) > 1:
                    text = ((i.select_one('div.compText')).text.strip()).split("·")[1]
                else:
                    text = ((i.select_one('div.compText')).text.strip())
                # append this as a dict into the result
                results.append({'query': keyword,
                                'link': link,
                                'title': title,
                                'text': text})
            except:
                print("Error in fetching data")
                continue

            DBobejct.insertQuery(keyword, searchengine, link, title, text)
        # returing list of dictionaries
        return results

    elif searchengine == 'Google':

        # using API for google search engine as the google changes they classed very frequently

        params = {
            "engine": "google",
            "num": "100",
            "q": keyword,
            "api_key": os.environ["SERP_API_KEY"]
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        results = []
        for i in organic_results:
            results.append({'query': keyword,
                            'link': i["link"],
                            'title': i["title"],
                            'text': i["snippet"]
                            })

        return results


    elif searchengine == 'DuckDuckGo':

        # completing the url using user defined query
        url = f'https://html.duckduckgo.com/html/'
        # creating a response object for storing all the information from the url
        resp = requests.post(url, data={'q': keyword, 'b': '', 'kl': 'us-en'}, headers={'user-agent': 'my-app/0.0.1'})
        # using beautiful soup converting response into a nested data structure
        soup = BeautifulSoup(resp.text, 'html.parser')
        # selecting all the classes which we gonna use to extract info we require
        tags = soup.select('div.results div.result.results_links.results_links_deep.web-result')

        # creating an empty list to store the results
        results = []


        for i in tags:

            try:
                # selecting url using href tags
                link = (i.select_one('a.result__snippet')).get('href', u'')
                # selecting title using h2 tags
                title = (i.select_one('h2.result__title a')).text
                # selecting text using result__snippet tags
                text = (i.select_one('a.result__snippet')).text
                # append this as a dict into the result
                results.append({'query': keyword,
                                'link': link,
                                'title': title,
                                'text': text})
            except:
                print("Error in fetching data")
                continue

            DBobejct.insertQuery(keyword, searchengine, link ,title, text)
            # Keyword, searchengine, URLs, Title, Data

        # returing list of dictionaries
        return results


# res= Search("iphone 14 pro", "duckduckgo")

# print(res)

    # allTitles = []
    #
    # try:
    #     urls = list(set(search(searchEngines.get(str(searchengine.lower()), None) + keyword)))
    #     print(urls)
    #
    #     if not urls == None:
    #         for i in tqdm(range(len(urls))):
    #             try:
    #
    #                 # Make a request to the webpage
    #                 # response = requests.get(urls[i])
    #                 response = urllib.request.urlopen(urls[i])
    #
    #                 # Parse the HTML content using Beautiful Soup
    #                 soup = BeautifulSoup(response.read(), 'html.parser')
    #
    #             except:
    #                 print("Authorization Failed \n")
    #
    #             # Find the data you want using Beautiful Soup methods
    #             try:
    #                 title = soup.title.text.strip()
    #                 try:
    #                     heading = soup.h1.text.strip()
    #                 except:
    #                     heading = 'Null'
    #
    #                 paragraphs = " "
    #                 for p in soup.find_all([ 'h2', 'p']):
    #                     paragraphs += re.sub('\W+', ' ', p.text.strip())
    #                     paragraphs += " "
    #                     # paragraphs = [p.text.strip() for p in soup.find_all('p')]
    #
    #                 # Print the data
    #                 print('Title:', title)
    #                 print('Heading:', heading)
    #                 # print("*" * 100)
    #                 print('Paragraphs:', paragraphs[:1000])
    #                 print("\n")
    #
    #                 # Checking if the data contains any ads sponsored
    #                 pattern = r'\b(ad|ads|advertisement|sponsor(ed)?)\b'
    #                 if re.search(pattern, paragraphs[:1000]):
    #                     print("The string contains ads or advertising data.")
    #                     break
    #
    #                 if title not in allTitles:
    #                     allTitles.append(title)
    #                     DBobejct.insertQuery(searchengine,keyword, urls[i], title, heading, paragraphs[:1000])
    #
    #                 else:
    #                     print("already title exists")
    #             except:
    #                 print("An exception occurred")
    #
    # except:
    #     print("Enter Correct Name")
