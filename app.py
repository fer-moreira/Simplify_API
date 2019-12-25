# FLASK
from flask import Flask,request, render_template_string,render_template
from core.engine import PageReader
import sys, os, codecs
import json as jsonparse
from flask_cors import CORS, cross_origin

from requests.exceptions import SSLError

app = Flask(__name__,template_folder='template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/get_article",methods=['GET','POST'])
def json_summary():
    try:
        headers = request.headers
        _url = headers['article-url']

        reader = PageReader()
        reader.url = _url
        json = reader.dump_json

        return json
    except SSLError:
        return jsonparse.dumps({"error":{"code":404,"text":"Not Found"}})
    except Exception:
        raise
        # return jsonparse.dumps({"error":{'code':203,'text':'Something in article is missing'}})

    # finally:
    #     return jsonparse.dumps({"error":{'code':204,'text':'Unknow Error'}})


@app.route("/get_html")
def html_summary ():
    url = request.args.get('target')

    reader = PageReader()
    reader.url = url
    json = reader.dump_json
    py_json = jsonparse.loads(json)
    

    return render_template("dump.html",article=py_json)


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