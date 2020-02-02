# Simplify API!

This repository contains the code for 'Simplify Journal' backend.

Base application for the 'Simplify Journal' react-native app, it is a flask app that does the whole process of getting the article, scrapping it all and returning a json

---

<br>


# Getting Started

    $ git clone https://github.com/zisongbr/Simplify_API.git
    $ cd Simplify_API
    $ pip install -r requirements.txt


# Starting server

### Windows:

    > set FLASK_ENV=development
    > set FLASK_APP=app.py
    > python app.py run
    * Running on http://localhost:5000/ (Press CTRL+C to quit)

### Linux:

    $ export FLASK_ENV=development
    $ export FLASK_APP=app.py
    $ python app.py run
    * Running on http://localhost:5000/ (Press CTRL+C to quit)


## Request JSON example

    import requests
    import json

    url = "http://127.0.0.1:5000/get_article"


    headers = {
        "article-url": "https://www.nytimes.com/2019/12/23/world/europe/russia-putin.html"
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)

<br>

# JSON:

    {
        "code": 200,
        "original_post": "https://www.theguardian.com/australia-news/2020/feb/01/terror-on-all-sides-inside-a-firestorm-tearing-through-the-australian-bush",
        "site_name": "the Guardian",
        "site_favicon": "https://www.theguardian.com/favicon.ico",
        "keywords": [
            "Bushfires",
            "Australia news",
            "Canberra",
            "Australian Capital Territory",
            "Natural disasters and extreme weather",
            "Wildfires",
            "Rural Australia"
        ],
        "article_title": "Terror on all sides: inside a firestorm tearing through the Australian bush",
        "article_description": "Guardian Australia reporter Christopher Knaus and photographer Mike Bowers join the Cowie family defending their property about 100km from Canberra",
        "article_image": "https://i.guim.co.uk/",
        "article_capitalize": "",
        "article_body": [
            {
                "is_img": false,
                "content": "Guardian Australia reporter Christopher Knaus and photographer Mike Bowers join the Cowie family defending their property about 100km from Canberra ",
                "props": []
            },
            {
                "is_img": false,
                "content": "Bushfires menace homes and lives – and firefighters warn winds will create new threats • Thomas Keneally: ‘These fires have changed us’",
                "props": [
                    {
                        "start": 0,
                        "steps": 88,
                        "type": "strong",
                        "text": "Bushfires menace homes and lives – and firefighters warn winds will create new threats"
                    },
                    {
                        "start": 89,
                        "steps": 48,
                        "type": "link",
                        "text": "• Thomas Keneally: ‘These fires have changed us’",
                        "href": "https://www.theguardian.com/australia-news/2020/feb/01/thomas-keneally-these-fires-have-changed-us"
                    }
                ]
            },
            {
        ]
    }