import requests
from bs4 import BeautifulSoup
import mysql.connector
from googlesearch import search

# Creating connection object
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="******",
    database="my_custom_bot"
)

# Printing the connection object
print(mydb)

cursor = mydb.cursor()

# Creating table to store search terms
cursor.execute("CREATE TABLE IF NOT EXISTS search_query (id INT AUTO_INCREMENT PRIMARY KEY, term VARCHAR(255))")

# Creating table to store search results
cursor.execute("CREATE TABLE IF NOT EXISTS search_query_results (id INT AUTO_INCREMENT PRIMARY KEY, term_id INT, source VARCHAR(255), header VARCHAR(255), url VARCHAR(255))")

# Creating a new table to store ad-free URLs
cursor.execute("CREATE TABLE  IF NOT EXISTS ad_free_urls (id INT AUTO_INCREMENT PRIMARY KEY,  term_id INT, source VARCHAR(255), header VARCHAR(255),  url VARCHAR(255))")

# Getting the search term from user
search_query = input("Enter Your search term: ")

# Inserting the search term into the database
add_term = "INSERT INTO search_query (term) VALUES (%s)"
data_term = (search_query,)
cursor.execute(add_term, data_term)
term_id = cursor.lastrowid
print(f"Inserted search term '{search_query}' with ID {term_id}")

# Building the Google search URL
num_results = 20
google_url = f"https://www.google.com/search?q={search_query}&num={num_results}"
yahoo_url = f"https://search.yahoo.com/search?p={search_query}&n={num_results}"
bing_url = f"https://www.bing.com/search?q={search_query}&count={num_results}"
duckduckgo_url = f"https://duckduckgo.com/html/?q={search_query}&kl=us-en&kp=-2&kam=osm&kac=-1&kn=1&k1=-1&kae=d"

# Storing the URLs and their corresponding sources in a dictionary
search_urls = {
    google_url: "Google",
    yahoo_url: "Yahoo",
    bing_url: "Bing",
    duckduckgo_url: "DuckDuckGo"
}

# Looping through each search engine URL
all_urls = []
all_headers = []
for url, source in search_urls.items():
    # Sending a GET request to the URL
    response = requests.get(url)

    # Parsing the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding all the search result links (identified by the <a> tag and the "href" attribute)
    search_results = soup.find_all("a")

    # Extracting the URLs from the search result links
    for result in search_results:
        url = result.get("href")
        header = result.text
        if url and header:
            if url.startswith("/url?q="):
                url = url[7:]  # Removing the "/url?q=" prefix
                url = url.split("&")[0]  # Removing any additional parameters
                all_urls.append(url)
                all_headers.append(header)

    # Inserting the URLs and headers into the database
    for i in range(len(all_urls)):
        add_url = "INSERT INTO search_query_results (term_id, header, url, source) VALUES (%s, %s, %s, %s)"
        data_url = (term_id, all_headers[i], all_urls[i], source)
        cursor.execute(add_url, data_url)
        if cursor.rowcount == 1:
            print(f"Inserted URL '{all_urls[i]}' with header '{all_headers[i]}' for search term '{search_query}' and source '{source}'")
        else:
            print(f"Failed to insert URL '{all_urls[i]}' with header '{all_headers[i]}' for search term '{search_query}' and source '{source}'")

    # Commiting the changes to the database
    mydb.commit()

    # Looping through the URLs and insert any not containing "/ad/" into the new table
    for i in range(len(all_urls)):
        if "/ad/" not in all_urls[i]:
            insert_query = "INSERT INTO ad_free_urls (term_id, source, header, url) VALUES (%s, %s, %s, %s)"
            data = (term_id, source, all_headers[i], all_urls[i])
            cursor.execute(insert_query, data)
            if cursor.rowcount == 1:
                print(f"Inserted ad-free URL '{all_urls[i]}' into ad_free_urls table for search term '{search_query}' and source '{source}'")
            else:
                print(f"Failed to insert ad-free URL '{all_urls[i]}' into ad_free_urls table for search term '{search_query}' and source '{source}'")

    # Commiting the changes to the database
    mydb.commit()


    # Looping through the URLs and insert any not containing "/ad/" into the new table
    for i in range(len(all_urls)):
        if "/ad/" not in all_urls[i]:
            # Make a GET request to the URL to retrieve the HTML content
            response = requests.get(all_urls[i])
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the text data from the first paragraph on the page
            paragraph = soup.find('p')
            text_data = paragraph.get_text() if paragraph else ''

            # Truncate the text data if it is too long for the column
            max_length = 65535  # Maximum length of the text_data column
            if len(text_data) > max_length:
                text_data = text_data[:max_length]

            insert_query = "INSERT INTO ad_free_urls (term_id, source, header, url, text_data) VALUES (%s, %s, %s, %s, %s)"
            data = (term_id, source, all_headers[i], all_urls[i], text_data)
            cursor.execute(insert_query, data)
            if cursor.rowcount == 1:
                print(f"Inserted ad-free URL '{all_urls[i]}' into ad_free_urls table for search term '{search_query}' and source '{source}'")
            else:
                print(f"Failed to insert ad-free URL '{all_urls[i]}' into ad_free_urls table for search term '{search_query}' and source '{source}'")

    # Commiting the changes to the database
    mydb.commit()




cursor.close()
mydb.close()
