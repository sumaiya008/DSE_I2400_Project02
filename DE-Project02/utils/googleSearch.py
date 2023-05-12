from utils.DbOps import DbOps
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import requests
from serpapi import GoogleSearch

databaseName = 'my_custom_bot'
tablename = 'scrapeddata'


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
        for i in tqdm(tags):
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
                # print("Error in fetching data")
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

        for i in tqdm(tags):
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
                # print("Error in fetching data")
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
            "api_key": "<apikey>" "get from - https://serpapi.com/"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        results = []

        for i in tqdm(organic_results):
            try:
                results.append({'query': keyword,
                                'link': i["link"],
                                'title': i["title"],
                                'text': i["snippet"]
                                })
            except:
                # print("Error in fetching data")
                continue
            DBobejct.insertQuery(keyword, searchengine, i["link"],i["title"], i["snippet"])
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


        for i in tqdm(tags):

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
                # print("Error in fetching data")
                continue

            DBobejct.insertQuery(keyword, searchengine, link ,title, text)
            # Keyword, searchengine, URLs, Title, Data

        # returing list of dictionaries
        return results

