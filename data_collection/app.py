import sys
import logging
from flask import Flask, json, request, render_template
from flask_cors import CORS, cross_origin

from data_collection.wikidata_scholars import (
    WikiDataScholars,
    get_scholar_id_from_name,
    Scholar,
)

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

wikidata = WikiDataScholars()


@app.route("/", methods=["GET"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def web():
    with open("./scholars.json", "r") as f:
        scholar_web_json = f.read()
    return json.dumps(scholar_web_json)


@app.route("/scholar/<scholar_name>", methods=["GET"])
@cross_origin(origin="localhost", headers=["Content-Type", "Authorization"])
def get_scholar(scholar_name):
    scholar_qid = get_scholar_id_from_name(scholar_name)
    if scholar_qid == "missing":
        return json.dumps({"scholars": []})
    scholars = wikidata.run(max_scholars=50, starting_scholars=[scholar_qid])
    return json.dumps({"scholars": list(map(Scholar.to_json, scholars))})
