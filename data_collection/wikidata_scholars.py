import json
from dataclasses import dataclass
from wikidata.client import Client
from datetime import datetime
import requests

from data_collection.mappings import name_to_attribute

WIKIDATA_IMAGE = "https://commons.wikimedia.org/wiki/File:"
Wiki_Client = Client()


@dataclass
class Scholar:
    id: str
    name: str
    image_link: str
    wiki_link: str
    field: str
    doctoral_advisors: []
    doctoral_students: []

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_link": self.image_link,
            "wiki_link": self.wiki_link,
            "field": self.field,
            "doctoral_advisor": self.doctoral_advisors,
            "doctoral_student": self.doctoral_students,
        }

    def convert_qids(self):
        self.doctoral_students = list(
            map(get_scholar_name_from_id, self.doctoral_students)
        )
        self.doctoral_advisors = list(
            map(get_scholar_name_from_id, self.doctoral_advisors)
        )


class WikiDataScholars:
    def __init__(
        self, scholar_json_file="scholars.json", debug_file="debug.txt",
    ):
        """
        Creates a new instance of a WikiDataScholar object. 

        starting_scholars: initial list of scholars to begin the web from
        scholar_json_file: file path for the JSON object of the web
        debug_file: file path for debug file
        max_scholars: how many scholars we want to scrape before exiting
        """
        self.debug = open(debug_file, "w+")
        self.debug.write(f"Moment of Instantiation: {datetime.now()}")

        self.scholar_json_file = scholar_json_file

    def run(self, max_scholars=0, starting_scholars=["Q222541"]):
        """Begin the scraping process for the web"""
        num_processed = 0
        to_process = starting_scholars
        seen_scholars = set()
        scholars_json = list()
        while to_process and max_scholars > num_processed:
            if not to_process[0] in seen_scholars:
                seen_scholars.add(to_process[0])
                cur_scholar_json = self.get_scholar_advisors_and_students(to_process[0])
                to_process.extend(cur_scholar_json.doctoral_advisors)
                to_process.extend(cur_scholar_json.doctoral_students)
                scholars_json.append(cur_scholar_json)
            to_process = to_process[1:]
            num_processed += 1
        return scholars_json

    def get_scholar_advisors_and_students(self, scholar_query_id):
        """string -> Scholar"""
        self.cur_scholar_id = scholar_query_id

        cur_scholar = Wiki_Client.get(scholar_query_id)
        scholar_name = self.get_name(cur_scholar)
        scholar_wiki_link = self.get_wiki_link(cur_scholar)
        scholar_image = self.get_image(cur_scholar)
        scholar_field = self.get_field(cur_scholar)
        scholar_advisors = self.get_advisors(cur_scholar)
        scholar_students = self.get_students(cur_scholar)

        self.debug.write(f"Scholar Name: {scholar_name}\n")
        self.debug.write(f"Scholar Query ID: {scholar_query_id}\n")
        print("Current Scholar: {} {}".format(scholar_name, scholar_query_id))

        return Scholar(
            scholar_query_id,
            scholar_name,
            scholar_image,
            scholar_wiki_link,
            scholar_field,
            scholar_advisors,
            scholar_students,
        )

    def get_value_from_attributes(self, desired_attr, attributes_object):
        """
        Takes in an object of scholar attributes and a desired attribute value
        to return. The desired attribute is mapped to a list of attributes 
        that lead to the values. This list is iterated over to retrieve 
        the desired value. 
        """
        try:
            current_object = attributes_object
            for attr in name_to_attribute[desired_attr]:
                current_object = current_object.__getitem__(attr)
            return current_object
        except (TypeError, KeyError):
            self.debug.write(f"NO {desired_attr}: {self.cur_scholar_id}\n")
            return ""

    def get_name(self, scholar):
        self.cur_scholar_id = scholar
        name = self.get_value_from_attributes("name", scholar.attributes)
        if not name:
            name = self.get_value_from_attributes("other_name", scholar.attributes)
            if not name:
                return self.get_value_from_attributes("title_name", scholar.attributes)
        else:
            return name

    def get_wiki_link(self, scholar):
        return self.get_value_from_attributes("wiki_link", scholar.attributes)

    def get_image(self, scholar):
        image_link = self.get_value_from_attributes("image_link", scholar.attributes)
        return WIKIDATA_IMAGE + image_link.replace(" ", "_")

    def get_field(self, scholar):
        return self.get_value_from_attributes("field", scholar.attributes)

    def get_advisors(self, scholar):
        advisors = list()
        for advisor in self.get_value_from_attributes("advisors", scholar.attributes):
            advisor_qid = self.get_value_from_attributes("scholar_qid", advisor)
            if advisor_qid:
                advisors.append(advisor_qid)
        return advisors

    def get_students(self, scholar):
        students = list()
        for student in self.get_value_from_attributes("students", scholar.attributes):
            student_qid = self.get_value_from_attributes("scholar_qid", student)
            if student_qid:
                students.append(student_qid)
        return students

    def finish_and_print(self, scholars):
        self.scholar_json = open(self.scholar_json_file, "w+")
        self.scholar_json.seek(0)
        self.scholar_json.truncate()

        self.scholar_json.write(
            json.dumps(
                {"scholars": list(map(Scholar.to_json, scholars))},
                indent=4,
                sort_keys=True,
            )
        )
        self.debug.close()
        self.scholar_json.close()


def get_scholar_id_from_name(name: str):
    """ str -> str (QID) """
    wiki_res = requests.get(
        f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1&format=json&titles={name}"
    )
    try:
        key = list(json.loads(wiki_res.content)["query"]["pages"].keys())[0]
        return json.loads(wiki_res.content)["query"]["pages"][key]["pageprops"][
            "wikibase_item"
        ]
    except KeyError:
        return json.loads('"missing"')


def get_scholar_name_from_id(qid: str):
    wd = WikiDataScholars()
    scholar = Wiki_Client.get(qid)
    return wd.get_name(scholar)
