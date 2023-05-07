from flask import Flask
from flask import request, jsonify
from utils.utils import spellChecker, preprocess
from googleSearch import DBobejct


# import pandas as pd

app = Flask(__name__)

@app.route('/index', methods=['GET','POST'])
def index():
    try:
        if request.values['keyword']:
            keyword= request.values['keyword']
            keyword = preprocess(keyword) #edited here
            
            correctSpell =spellChecker('New yor  City')
            print(correctSpell)
            if correctSpell != None:
                print("Spelling ")
                res = DBobejct.searchKeyword(correctSpell)
            else:
                res = DBobejct.searchKeyword(keyword)

            print(res)
            return jsonify(
                {"message": res ,
                 "status": "success"}), 200

        else:
            pass


    except Exception as ex:
        return jsonify(
            {"message": "Page Not Found", "status": "fail"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port =5005)