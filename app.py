# FLASK
from flask import Flask, request, render_template_string, render_template, Response
from flask_cors import CORS, cross_origin

# EXCEPTIONS
from requests.exceptions import SSLError, ConnectionError, MissingSchema

# SYSTEM
from core.parser import PageParser
from core.auth import Authentication

import sys, os, codecs, traceback, json

app = Flask(__name__)
cors = CORS(app)

app.config.update(
    CORS_HEADERS        = 'Content-Type',
    PORT                = int(os.environ.get("PORT", 5000)),
    DEBUG               = True if int(os.environ.get("DEBUG", 0)) == 1 else False,
    FLASK_ENV           = os.environ.get("FLASK_ENV", "DEV"),
    PARSER_USER         = os.environ.get("PARSER_USER", None),
    PARSER_PASSWORD     = os.environ.get("PARSER_PASSWORD", None),
    PARSER_CIPHER_KEY   = os.environ.get("PARSER_CIPHER_KEY", None)
)


@app.route("/parser/json", methods=['GET'])
def json_summary():
    try:
        headers = request.headers
        ENCODED_CREDENTIALS = headers['X_ENC_KEY']

        auth = Authentication(
            app.config["PARSER_CIPHER_KEY"],
            {app.config["PARSER_USER"] : app.config["PARSER_PASSWORD"]}
        )

        is_auth = auth.is_auth(ENCODED_CREDENTIALS)

        if is_auth:
            ARTICLE_URL = headers['ARTICLE_URL']
            reader = PageParser(ARTICLE_URL)
            dump = reader.dump_json()
            return Response(response=dump,status=200,mimetype="application/json")
        else:
            return Response(response=json.dumps({"error": {'code': 403, 'text': "FORBIDDEN"}}), status=403, mimetype="application/json")

    except Exception as r:
        return Response(response=json.dumps({"error": {'code': 505, 'text': r.__class__.__name__, 'log': r.args}}),status=505,mimetype="application/json")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=app.config["DEBUG"])
