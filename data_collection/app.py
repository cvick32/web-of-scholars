import sys
import logging
from flask import Flask, json, request, render_template
from flask_cors import CORS, cross_origin

from wikidata_scholars import WikiDataScholars, get_scholar_id_from_name

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

wikidata = WikiDataScholars()


@app.route("/", methods=["GET"])
def home():
    return "hello"


@app.route("/scholar/<scholar_name>", methods=["GET"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def send_jeopardy_json(scholar_name):
    scholar_qid = get_scholar_id_from_name(scholar_name)
    scholar = wikidata.get_scholar_advisors_and_students(scholar_qid)
    return json.dumps(scholar.to_json())
