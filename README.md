# Simplify please!

Aplicação base para o app 'Simplify Journal', ele é um app em flask que faz todo o processo de pegar a matéria, fazer o scrap todo dela e retornar um json com o seguinte formato




### Exemplo: 'https://www.nytimes.com/2019/12/23/world/europe/russia-putin.html'

    {
    "origin": "https://www.nytimes.com/2019/12/23/world/europe/russia-putin.html",
    "title": "Russia Is a Mess. Why Is Putin Such a Formidable Enemy?",
    "pre_title": "Its economy is sputtering and its young are frustrated, but with America and Europe in tumult, Russia and its leader of two decades are on a roll.",
    "site_origin": "",
    "site_image": "favico.ico",
    "post_image": "image.jpg",
    "post_img_alt": "President Vladimir V. Putin at his annual news conference in Moscow last week.",
    "keywords": [
    "Putin",
    " Vladimir V",
    "Russia",
    "Politics and Government"
    ],
    "body": [
            {
            "text": "Eu sou o primeiro paragrafo da materia",
            "strong": true,
            "a": false,
            "a_link": ""
            }
            {...}
        ]
    }