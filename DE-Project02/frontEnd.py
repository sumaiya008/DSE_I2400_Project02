from flask import render_template
from flask import Flask
from flask import request
from utils.utils import spellChecker, word_freq
from googleSearch import DBobejct, Search
from DbOps import DbOps

app = Flask(__name__)

databaseName = 'my_custom_bot'
tablename = 'scrapeddata'


# data = [('iphone 14 pro', 'duckduckgo', 'https://www.apple.com/iphone-14-pro/', 'iPhone 14 Pro and iPhone 14 Pro Max - Apple', None, 'iPhone 14 Pro can detect a severe car crash, then call 911 and notify your emergency contacts. 6 Hardware sensors and advanced motion algorithms identify signs of a crash — including sudden changes in speed, direction, and cabin pressure. Over 1 million hours of real‑world driving and crash data helps iPhone recognize accidents'), ('iphone 14 pro', 'duckduckgo', 'https://www.apple.com/iphone-14-pro/specs/', 'iPhone 14 Pro and 14 Pro Max - Technical Specifications - Apple', None, 'The iPhone 14 Pro display has rounded corners that follow a beautiful curved design, and these corners are within a standard rectangle. When measured as a standard rectangular shape, the screen is 6.12 inches diagonally (actual viewable area is less). Super Retina XDR display 6.7‑inch (diagonal) all‑screen OLED display')]
# data1 = "Shubham"

# ALTER TABLE scrapeddata ADD FULLTEXT(Keyword);


@app.before_first_request
def before_first_request(alterTable=None):
    # Calling database object
    DBobejct = DbOps(databaseName, tablename)
    # connecting to database
    DBobejct.connect()
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

    # DBobejct.alterTable()


@app.route('/')
def index():
    if (request.method == 'GET') or (request.method == 'POST'):
        return render_template('index.html')


@app.route('/view')
def view():
    # print(keyword)
    if (request.method == 'GET') or (request.method == 'POST'):
        userInput = request.args.get('user_input')
        print(userInput)

        for engine in ['Bing', 'Yahoo', 'DuckDuckGo']:
            Search(userInput, engine)


        keyword = userInput
        correctSpell = spellChecker(keyword)
        # print(correctSpell)

        if correctSpell != None:
            print("Corrected Spelling ", correctSpell)
            res = DBobejct.searchKeyword(correctSpell)
        else:
            res = DBobejct.searchKeyword(keyword)

        sorted_data = word_freq(userInput, res)
        # print(sorted_data)

        return render_template('result.html', content=sorted_data)


if __name__ == '__main__':
    app.run(debug=True)
