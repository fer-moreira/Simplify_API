# FLASK
from flask import Flask,request, render_template_string,render_template, Response
from core.parser import PageParser
import sys, os, codecs
import json as jsonparse
from flask_cors import CORS, cross_origin

from requests.exceptions import SSLError, ConnectionError, MissingSchema

app = Flask(__name__,template_folder='template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



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

    except SSLError:        json = jsonparse.dumps({"error":{"code":400,"text":"Article not found"}})
    except AttributeError:  json = jsonparse.dumps({"error":{'code':400,'text':'Something in article is missing'}})
    except ConnectionError: json = jsonparse.dumps({"error":{'code':404,'text':'Failed to make connection, URL not exists'}})
    except MissingSchema:   json = jsonparse.dumps({"error":{'code':404,'text':'Not valid URL'}})
    except TypeError:       json = jsonparse.dumps({"error":{'code':404,'text':'Misspell URL'}})
    except Exception as r:  json = jsonparse.dumps({"error":{'code':505,'text':r.__class__.__name__,'log':r.args}})

    return json

@app.route("/parser/json",methods=['GET','POST'])
def json_summary():
    try:
        headers = request.headers
        _url = headers['article-url']
        json = try_get_article(_url)
        return Response(response=json,status=200, mimetype="application/json")

    except KeyError  as r: 
        err = jsonparse.dumps({"error":{"code":400,"text":"Missing headers",'log':r.args}})
        return Response(response=err,status=400, mimetype="application/json")
    except Exception as r: 
        err = jsonparse.dumps({"error":{'code':505,'text':r.__class__.__name__,'log':r.args}})
        return Response(response=err,status=505, mimetype="application/json")


@app.route("/")
def admin_page ():
    html = '''
    <div style="display: flex;justify-content: center;align-items: center;height: 100%;width: 100%;">
        <div style="display: flex; align-items: center;justify-content: center;">
            <h1 style="font-size: 50px;">
            Simplify is working fine! :)
            </h1>
        </div>
    </div>
    '''
    return render_template_string(html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)