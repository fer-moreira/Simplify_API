# FLASK
from flask import Flask,request, render_template_string,render_template, Response
from flask_cors import CORS, cross_origin

# EXCEPTIONS
from requests.exceptions import SSLError, ConnectionError, MissingSchema

# SYSTEM
from core.parser import PageParser
from core.auth import Authentication

import sys, os, codecs, traceback
import json as jsonparse

app = Flask(__name__,template_folder='template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

PORT = int(os.environ.get("PORT", 5000))
DEBUG = int(os.environ.get("DEBUG", 1))
DEBUG_ENV = int(os.environ.get("DEBUG_ENV", 0))
ENV = os.environ.get("ENV", "Development")
MASTER_KEY = os.environ.get("MASTER_KEY", None)
MASTER_USER = os.environ.get("MASTER_USER", None)
MASTER_PASSWORD = os.environ.get("MASTER_PASSWORD", None)

def try_get_article (url):
    """Try requests selected url and dump its content in json

    Parameters:
    url (string): Selected URL

    Returns:
    json: Scraped page as json

   """
    try:
        reader = PageParser()
        reader.url = url
        json = reader.dump_json

        # fj = open(r"./template/dump.json","r").read()
        # json = fj

    except SSLError as r:        json = jsonparse.dumps({"error":{'code':404,'text': str(r)}})
    except AttributeError as r:  json = jsonparse.dumps({"error":{'code':404,'text': str(r)}})
    except ConnectionError as r: json = jsonparse.dumps({"error":{'code':404,'text': str(r)}})
    except MissingSchema as r:   json = jsonparse.dumps({"error":{'code':404,'text': str(r)}})
    except TypeError as r:       json = jsonparse.dumps({"error":{'code':404,'text': str(r)}})
    except Exception as r:       json = jsonparse.dumps({"error":{'code':505,'text':r.__class__.__name__,'log':r.args}})
    
    return json

@app.route("/parser/json",methods=['GET','POST'])
def json_summary():
    try:
        headers = request.headers

        REACT_APP_PARSER_KEY        = headers['REACT_APP_PARSER_KEY']
        REACT_APP_PARSER_USER       = headers['REACT_APP_PARSER_USER']
        REACT_APP_PARSER_PASSWORD   = headers['REACT_APP_PARSER_PASSWORD']
        REACT_APP_ARTICLE_URL       = headers['REACT_APP_ARTICLE_URL']

        auth = Authentication({
            "MASTER_KEY":MASTER_KEY,
            "MASTER_USER":MASTER_USER,
            "MASTER_PASSWORD":MASTER_PASSWORD
        }, {
            "REACT_APP_PARSER_KEY":REACT_APP_PARSER_KEY,
            "REACT_APP_PARSER_USER":REACT_APP_PARSER_USER,
            "REACT_APP_PARSER_PASSWORD":REACT_APP_PARSER_PASSWORD,
        })

        if not auth.is_auth():
            return Response(
                response=jsonparse.dumps({"error":{'code':403,'text':"forbidden",}}),
                status=403, 
                mimetype="application/json"
            )
        else:
            json = try_get_article(str(REACT_APP_ARTICLE_URL))
            return Response(
                response=json, 
                status=200, 
                mimetype="application/json"
            )

    except KeyError  as r: 
        return Response(
            response=jsonparse.dumps({
                "error":{
                    "code":400,
                    "text":"MISSING HEADERS",
                    'log':r.args
                }
            }),
            status=400, 
            mimetype="application/json"
        )
    except Exception as r: 
        return Response(
            response=jsonparse.dumps({"error":{'code':505,'text':r.__class__.__name__,'log':r.args}}),
            status=505,
            mimetype="application/json"
        )

@app.route("/environment")
def environment ():
    if DEBUG == 1 and DEBUG_ENV == 1:
        json = jsonparse.dumps({
            "environment" : ENV,
            "port": PORT,
            "debug":DEBUG,
            "variables" : {
                "MASTER_KEY":MASTER_KEY,
                "MASTER_USER":MASTER_USER,
                "MASTER_PASSWORD":MASTER_PASSWORD,
                "MASTER_KEY":MASTER_KEY,
            }
        })

        return Response(response=json,status=200, mimetype="application/json")
    
    return Response(
        response=jsonparse.dumps({"error":{'code':403,'text':"FORBIDDEN"}}),
        status=403, 
        mimetype="application/json")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)