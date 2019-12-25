# FLASK
from flask import Flask,request, render_template_string,render_template
from core.engine import PageReader
import sys, os, codecs
import json as jsonparse
from flask_cors import CORS, cross_origin

from requests.exceptions import SSLError, ConnectionError, MissingSchema

app = Flask(__name__,template_folder='template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



def try_GetArticleData (_url):
    try:
        reader = PageReader()
        reader.url = _url
        json = reader.dump_json

    except SSLError: json = jsonparse.dumps(       {"error":{"code":400,"text":"Article not found"}})
    except AttributeError:  json = jsonparse.dumps({"error":{'code':400,'text':'Something in article is missing'}})
    except ConnectionError: json = jsonparse.dumps({"error":{'code':404,'text':'Failed to make connection, URL not exists'}})
    except MissingSchema:   json = jsonparse.dumps({"error":{'code':404,'text':'Not valid URL'}})
    except:                 json = jsonparse.dumps({"error":{'code':505,'text':'Unknow Error'}})

    return json

@app.route("/get_article",methods=['GET','POST'])
def json_summary():
    headers = request.headers
    _url = headers['article-url']
    json = try_GetArticleData(_url)
    return json


@app.route("/get_html")
def html_summary ():
    url = request.args.get('target')
    json = try_GetArticleData(url)

    return render_template("dump.html",article=jsonparse.loads(json))


@app.route("/")
def admin_page ():
    html = '''
    <div style="display: flex;justify-content: center;align-items: center;height: 100%;width: 100%;">
        <div style="display: flex; align-items: center;justify-content: center;">
            <h1 style="font-size: 50px;">Heroku working fine! :)</h1>
        </div>
    </div>
    '''
    return render_template_string(html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)