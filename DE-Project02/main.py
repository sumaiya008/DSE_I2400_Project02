from googleSearch import Search
from DbOps import DbOps

databaseName = 'my_custom_bot'
tablename = 'scrapeddata'



#Calling database object
DBobejct = DbOps(databaseName, tablename)
#connecting to database
DBobejct.connect()

# Input Keyword to Google Search Engine
# keyword = input("Enter the search keyword : ")
keyword = 'Shubham Khandale'
# searchEngine = input("Enter the search Engine : \n"
#                      "1. Google\n"
#                      "2. Bing\n"
#                      "3. Yahoo\n"
#                      "4. DuckDuckGo")
searchEngine = 'Yahoo'
# query = "iphone 13"
# searchEngine = "Google"

# Check if database exists
if DBobejct.database_exists():
    print("Database exists........")
else:
    print("Error while connecting to database")

# Check if Table Exists if not the it will create the table
if DBobejct.checkTable():
    pass
else:
    DBobejct.createTable()

# Calling Google Search Engine
# googleSearch(query, searchEngine)
Search(keyword, searchEngine)

# query = input("Enter the search query : ")

res= DBobejct.searchKeyword(keyword)
print(res)

# res= Search("iphone 14 pro", "duckduckgo")
# #
# print(res)



