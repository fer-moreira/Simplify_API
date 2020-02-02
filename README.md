# Simplify API!

This repository has all the code needed to communicate with <a href="https://github.com/zisongbr/SimplifyJournal_APP">'Simplify Journal'</a> react-native application. this server provides an API used to scrap and selected URL and return all the content as JSON.

<br>


# Getting Started

    $ git clone https://github.com/zisongbr/Simplify_API.git
    $ cd Simplify_API
    $ pip install -r requirements.txt

<br>

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

</br>

# Create and deploy to Heroku

    $ git clone https://github.com/zisongbr/Simplify_API.git
    $ cd Simplify_API
    $ git init | or fork
    $ heroku apps:create example_name
    
    * Creating ⬢ example... done
    * https://example.herokuapp.com/ | https://git.heroku.com/example.git
    * Git remote heroku added


</br>

# Request JSON example

    import requests

    url = "http://localhost:5000/get_article"


    headers = {
        "article-url": "https://www.nytimes.com/2019/12/23/world/europe/russia-putin.html"
    }

    response = requests.request("GET", url, headers=headers)
    JSON = response.text

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
