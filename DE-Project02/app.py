
from flask import render_template
from flask import Flask
from flask import request
from utils.utils import spellChecker, word_freq
from utils.googleSearch import DBobejct, Search
from utils.DbOps import DbOps
from flask_ngrok import run_with_ngrok

import logging, ngrok

logging.basicConfig(level=logging.INFO)
tunnel = ngrok.werkzeug_develop()

app = Flask(__name__)
run_with_ngrok(app)

databaseName = 'my_custom_bot'
tablename = 'scrapeddata'


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

    DBobejct.alterTable()


@app.route('/')
def index():
    if (request.method == 'GET') or (request.method == 'POST'):
        return render_template('index.html')


@app.route('/view')
def view():
    if (request.method == 'GET') or (request.method == 'POST'):
        userInput = request.args.get('user_input')

        if userInput == '':
            return render_template('pageNotFound.html')

        for engine in ['Bing', 'Yahoo', 'DuckDuckGo', 'Google']:
            Search(userInput, engine)

        keyword = userInput
        correctSpell = spellChecker(keyword)

        if correctSpell != None:
            res = DBobejct.searchKeyword(correctSpell)
        else:
            res = DBobejct.searchKeyword(keyword)

        sorted_data = word_freq(userInput, res)

        return render_template('result.html', content=sorted_data)


if __name__ == '__main__':
    app.run()
