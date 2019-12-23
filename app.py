# FLASK
from flask import Flask,request, render_template_string
from core.engine import PageReader
import sys, os, codecs, json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/get_article",methods=['GET','POST'])
def json_summary():
    headers = request.headers
    _url = headers['article-url']

    reader = PageReader()
    reader.url = _url
    json = reader.dump_json

    return json

@app.route("/admin")
def admin_page ():
    html = '''
    <div style="display: flex;justify-content: center;align-items: center;height: 100%;width: 100%;">
        <div style="display: flex; align-items: center;justify-content: center;">
            <h1 style="font-size: 50px;">Heroku working fine! :)</h1>
        </div>
    </div>
    '''
    return render_template_string(html)

@app.route("/page_html")
def html_summary ():
    reader = PageReader()
    reader.url = "https://www.nytimes.com/2019/12/23/world/europe/russia-putin.html"
    html = reader.dump_html

    pattern = ''' 
    <div style="display: flex; align-items: center; justify-content: center;"><div style="width: 40%;display: flex;flex-direction: column; align-items: center; justify-content: center;">{0}</div></div>
    '''.format(str(html))

    return render_template_string(pattern)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)