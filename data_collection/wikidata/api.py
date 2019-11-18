import json
from wikidata.client import Client

property_map = {
    "doctoral_advisor": "P184",
    "doctoral_student": "P185",
    "field": "P101",
    "image": "P18",
}

WIKIDATA_IMAGE = "https://commons.wikimedia.org/wiki/File:"


class WikiDataScholars:
    def __init__(self):
        # open log files
        self.debug = open("debug.txt", "w+")
        self.debug.seek(0)
        self.debug.truncate()

        self.scholar_json = open("scholars.json", "w+")
        self.scholar_json.seek(0)
        self.scholar_json.truncate()

        self.Wiki_Client = Client()

        self.to_process = ["Q222541"]
        self.seen_scholars = set()
        self.all_scholars = list()

    def run(self):
        while self.to_process:
            if not self.to_process[0] in self.seen_scholars:
                self.seen_scholars.add(self.to_process[0])
                self.get_scholar_advisors_and_students(self.to_process[0])
            self.to_process = self.to_process[1:]
        self.finish_and_print()

    def get_scholar_advisors_and_students(self, scholar_query_id):
        cur_scholar = self.Wiki_Client.get(scholar_query_id)
        print(scholar_query_id)

        scholar_name = self.get_name(cur_scholar, scholar_query_id)
        scholar_wiki_link = self.get_wiki_link(cur_scholar, scholar_query_id)
        scholar_image = self.get_image(cur_scholar, scholar_query_id)
        scholar_field = self.get_field(cur_scholar, scholar_query_id)
        scholar_advisors = self.get_advisors(cur_scholar, scholar_query_id)
        scholar_students = self.get_students(cur_scholar, scholar_query_id)

        cur_scholar_json = {
            "id": scholar_query_id,
            "name": scholar_name,
            "image": scholar_image,
            "link": scholar_wiki_link,
            "field": scholar_field,
            "doctoral_advisor": scholar_advisors,
            "doctoral_student": scholar_students,
        }
        self.all_scholars.append(cur_scholar_json)

    def get_name(self, scholar, query_id):
        try:
            return scholar.attributes["aliases"]["en"][0]["value"]
        except (TypeError, KeyError):
            try:
                return scholar.attributes["labels"]["en"]["value"]
            except (TypeError, KeyError):
                self.debug.write("NO NAME: " + query_id + "\n")
                return ""

    def get_wiki_link(self, scholar, query_id):
        try:
            return scholar.attributes["sitelinks"]["enwiki"]["url"]
        except (TypeError, KeyError):
            self.debug.write("NO WIKI LINK: " + query_id + "\n")
            return ""

    def get_image(self, scholar, query_id):
        try:
            return WIKIDATA_IMAGE + scholar.attributes["claims"][property_map["image"]
                                                                 ][0]["mainsnak"]["datavalue"]["value"].replace(" ", "_")
        except (TypeError, KeyError):
            self.debug.write("NO IMAGE: " + query_id + "\n")
            return ""

    def get_field(self, scholar, query_id):
        try:
            return scholar.attributes["claims"][property_map["field"]][0
                                                                       ]["mainsnak"]["datavalue"]["value"]["id"]
        except (TypeError, KeyError):
            self.debug.write("NO FIELD: " + query_id + "\n")
            return ""
    
    def get_advisors(self, scholar, query_id):
        advisors = list()
        try:
            for advisor in scholar.attributes["claims"][property_map["doctoral_advisor"]]:
                try:
                    advisor_qid = advisor["mainsnak"]["datavalue"]["value"]["id"]
                    self.to_process.append(advisor_qid)
                    advisors.append(advisor_qid)
                except KeyError:
                    pass
        except KeyError:
            pass
        return advisors
    
    def get_students(self, scholar, query_id):
        students = list()
        try:
            for student in scholar.attributes["claims"][property_map["doctoral_student"]]:
                try:
                    student_qid = student["mainsnak"]["datavalue"]["value"]["id"]
                    self.to_process.append(student_qid)
                    students.append(student_qid)
                except KeyError:
                    pass
        except KeyError:
            pass
        return students

    def finish_and_print(self):
        self.scholar_json.write(json.dumps(
            self.all_scholars, indent=4, sort_keys=True))
        self.debug.close()
        self.scholar_json.close()


scholar_web = WikiDataScholars()
scholar_web.run()
