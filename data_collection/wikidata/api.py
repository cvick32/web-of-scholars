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
        # try to get scholar's name
        try:
            cur_scholar_name = cur_scholar.attributes["aliases"]["en"][0]["value"]
            print(cur_scholar_name)
        except (TypeError, KeyError):
            try:
                cur_scholar_name = cur_scholar.attributes["labels"]["en"]["value"]
                print(cur_scholar_name)
            except (TypeError, KeyError):
                self.debug.write("NO NAME: " + scholar_query_id)
                # if this scholar does not have a name, do nothing else
                return
        # try to get scholar's image
        try:
            cur_scholar_image = WIKIDATA_IMAGE + cur_scholar.attributes["claims"][
                property_map["image"]
            ][0]["mainsnak"]["datavalue"]["value"].replace(" ", "_")
        except (TypeError, KeyError):
            self.debug.write("NO IMAGE: " + scholar_query_id)
            cur_scholar_image = ""
        # try to get scholar's link to wiki, only accept english wiki currently
        try:
            cur_scholar_link = cur_scholar.attributes["sitelinks"]["enwiki"]["url"]
        except (TypeError, KeyError):
            self.debug.write("NO WIKI LINK: " + scholar_query_id)
            cur_scholar_link = ""

        # try to get scholar's academic field
        try:
            cur_scholar_field = cur_scholar.attributes["claims"][property_map["field"]][
                0
            ]["mainsnak"]["datavalue"]["value"]["id"]
        except (TypeError, KeyError):
            self.debug.write("NO FIELD: " + scholar_query_id)
            cur_scholar_field = ""

        cur_scholar_json = {
            "id": scholar_query_id,
            "name": cur_scholar_name,
            "image": cur_scholar_image,
            "link": cur_scholar_link,
            "field": cur_scholar_field,
            "doctoral_advisor": list(),
            "doctoral_student": list(),
        }

        # try to get scholar advisors
        try:
            for advisor in cur_scholar.attributes["claims"][
                property_map["doctoral_advisor"]
            ]:
                advisor_qid = advisor["mainsnak"]["datavalue"]["value"]["id"]
                self.to_process.append(advisor_qid)
                cur_scholar_json["doctoral_advisor"].append(advisor_qid)
        except KeyError:
            pass

        # try to get scholar students
        try:
            for student in cur_scholar.attributes["claims"][
                property_map["doctoral_student"]
            ]:
                student_qid = student["mainsnak"]["datavalue"]["value"]["id"]
                self.to_process.append(student_qid)
                cur_scholar_json["doctoral_student"].append(student_qid)
        except KeyError:
            pass

        self.all_scholars.append(cur_scholar_json)

    def finish_and_print(self):
        self.scholar_json.write(json.dumps(self.all_scholars, indent=4, sort_keys=True))
        self.debug.close()
        self.scholar_json.close()


scholar_web = WikiDataScholars()
scholar_web.run()
