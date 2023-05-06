
import requests as r
import bs4
import mysql.connector
import re


'''
Nikhita Kannam
'''

engine=input("Enter either Google or Bing or Yahoo: ").lower()


if engine == 'google':
    term = input("Enter a Google search query: ")
    url = 'https://www.google.com/search?q=' + term

    request_result=r.get( url )
    
    soup = bs4.BeautifulSoup(request_result.text,"html.parser")
    link = soup.find_all("a")

    for i in link:
        final_text_data = []
        href = i.get('href')
        if "url?q=" in href:
            heading = i.find_all('h3')
            text = i.find('p')
            if len(heading) >= 1:
                get_link = i.get('href')
                final = get_link.split("?q=")[1].split("&sa=U")[0]

                new_url = final
                request_result2=r.get(new_url)
                soup2 = bs4.BeautifulSoup(request_result2.text,"html.parser")
                soup2.prettify()
                text_data = soup2.select("p")[:5]
                for text in text_data:
                    final_text_data.append(text.get_text())
                title = heading[0].getText()

   
                final_text_data_1 = 'No Description'
                for i in range(len(final_text_data)):
                    final_text_data_1 = final_text_data[i]
                
                
                data_array= [term, 'Google', title, final, final_text_data_1]
                addurl = 'INSERT INTO search_result (term, search_engine, title, url, text_data) VALUES (%s, %s, %s, %s, %s)'

                try:
                    database = mysql.connector.connect(
                    host='localhost', database='my_custom_bot', user = 'root', password='Nikki@25first')
                    
                    cursor = database.cursor()
                    cursor.execute(addurl,data_array)
                    database.commit()
                    print('Success')

                except Exception as e:
                    print('Error', e)


elif engine == 'bing':
    bing_term = input("Enter Bing Search Query: ")
    bing_url="https://www.bing.com/search?q=" + bing_term

    bheaders={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

    bing_request=r.get(bing_url,headers=bheaders)
    b_soup = bs4.BeautifulSoup(bing_request.text, 'html.parser')

    data_block = b_soup.find_all("li",{"class":"b_algo"})[:10]
    final_text_data_b=[]

    for i in range(len(data_block)):
        final_text_data = []
        if len(data_block) >= 1:
            title_bing=data_block[i].find("a").text

            yahoo_link=data_block[i].find("a")
            final_link = yahoo_link.get("href")

            text_data=data_block[i].find("p",{"class":"b_lineclamp3 b_algoSlug"}) or data_block[i].find("p",{"class":"b_lineclamp2 b_algoSlug"})
            if text_data is None:
                text_data = 'No Description'
            else:
                text_data = text_data.get_text()


            data_array= [bing_term, 'Bing', title_bing, final_link, text_data]
            addurl = 'INSERT INTO search_result (term, search_engine, title, url, text_data) VALUES (%s, %s, %s, %s, %s)'

            try:
                    database = mysql.connector.connect(
                    host='localhost', database='my_custom_bot', user = 'root', password='Nikki@25first')
                    
                    cursor = database.cursor()
                    cursor.execute(addurl,data_array)
                    database.commit()
                    print('Success')

            except Exception as e:
                print('Error', e)



elif engine == 'yahoo':
    yahoo_headers = {'User-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}
    yahoo_term = input("Enter Yahoo Search Query: ")

    url_yahoo = 'https://search.yahoo.com/search?p=' +yahoo_term

    request_yahoo = r.get(url_yahoo,headers=yahoo_headers).text
    soup_yahoo = bs4.BeautifulSoup(request_yahoo, 'lxml')


    data_block =  soup_yahoo.findAll('div',class_=re.compile("dd algo algo-sr relsrch"))

    if not soup_yahoo.find_all('ol',{'class':'scta reg searchCenterTopAds'}):

        for result in data_block:
            title = result.find("h3",{"class":"title"}).text
            titlefinal = re.split('- | > |\|  ', title)[-1]
            link_yahoo = result.find('h3').a['href']
            desc = result.find('div',class_='compText aAbs')
            if desc == None:
                desc = 'No Description'
            else:
                desc = desc.text
                
        
            data_array= [yahoo_term, 'Yahoo', title, link_yahoo, desc]
            addurl = 'INSERT INTO search_result (term, search_engine, title, url, text_data) VALUES (%s, %s, %s, %s, %s)'

            try:
                    database = mysql.connector.connect(
                    host='localhost', database='my_custom_bot', user = 'root', password='Nikki@25first')
                    
                    cursor = database.cursor()
                    cursor.execute(addurl,data_array)
                    database.commit()
                    print('Success')

            except Exception as e:
                print('Error', e) 

        

            
    



           





