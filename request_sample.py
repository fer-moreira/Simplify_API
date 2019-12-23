import requests
import json
import codecs

url = "http://127.0.0.1:5000/get_article"


headers = {
    "article-url": "https://www.nytimes.com/2019/12/23/world/europe/russia-putin.html"
}

response = requests.request("GET", url, headers=headers)
json = response.text

file = codecs.open(r"debug.html","w+","utf-8")
file.write(str(json))