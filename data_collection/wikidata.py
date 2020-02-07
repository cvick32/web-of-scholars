import json
from wikidata.client import Client

string_to_wikidata_key = {
    "doctoral_advisor": "P184",
    "doctoral_student": "P185",
    "field": "P101",
    "image": "P18",
}



WIKIDATA_IMAGE = "https://commons.wikimedia.org/wiki/File:"

class WikiDataScholars:
    def __init__(self, starting_scholars=["Q222541"], scholar_json_file="scholars.json", debug_file="debug.txt", max_scholars=0, bounded_huh=True):
        """
        Creates a new instance of a WikiDataScholar object. 

        starting_scholars: initial list of scholars to begin the web from
        scholar_json_file: file path for the JSON object of the web
        debug_file: file path for debug file
        max_scholars: how many scholars we want to scrape before exiting
        bounded_huh: do we want to stop on a bound?
        """
        self.debug = open(debug_file, "w+")
        self.debug.seek(0)
        self.debug.truncate()

        self.scholar_json = open(scholar_json_file, "w+")
        self.scholar_json.seek(0)
        self.scholar_json.truncate()

        self.Wiki_Client = Client()

        self.to_process = starting_scholars
        self.seen_scholars = set()
        self.all_scholars = list()

        self.max_scholars = max_scholars
        self.bounded_huh = bounded_huh

        self.num_processed = 0

    def run(self):
        """Begin the scraping process for the web."""
        while self.to_process:
            if self.bounded_huh and self.num_processed >= self.max_scholars:
                break
            if not self.to_process[0] in self.seen_scholars:
                self.seen_scholars.add(self.to_process[0])
                self.get_scholar_advisors_and_students(self.to_process[0])
            self.to_process = self.to_process[1:]
            self.num_processed += 1
        self.finish_and_print()

    def get_scholar_advisors_and_students(self, scholar_query_id):
        cur_scholar = self.Wiki_Client.get(scholar_query_id)

        scholar_name      = self.get_name(cur_scholar, scholar_query_id)
        scholar_wiki_link = self.get_wiki_link(cur_scholar, scholar_query_id)
        scholar_image     = self.get_image(cur_scholar, scholar_query_id)
        scholar_field     = self.get_field(cur_scholar, scholar_query_id)
        scholar_advisors  = self.get_advisors(cur_scholar, scholar_query_id)
        scholar_students  = self.get_students(cur_scholar, scholar_query_id)

        self.debug.write(f"Scholar Name: {scholar_name}\n")
        self.debug.write(f"Scholar Query ID: {scholar_query_id}\n")

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

    
    def get_any_from_attributes(self, attributes, items, desired_attr, query_id):
        try:
            current_attr = attributes
            for item in items:
                current_attr = current_attr.__getitem__(item)
            return current_attr
        except (TypeError, KeyError):
            self.debug.write(f"NO {desired_attr}: {query_id}\n")
            return ""
    
    def get_name(self, scholar, query_id):
        name = self.get_any_from_attributes(scholar.attributes, ["aliases", "en", 0, "value"], "name", query_id)
        if not name:
            return self.get_any_from_attributes(scholar.attributes, ["labels", "en", "value"], "name", query_id)
        else:
            return name

    def get_wiki_link(self, scholar, query_id):
        return self.get_any_from_attributes(scholar.attributes, ["sitelinks", "enwiki", "url"], "wiki_link", query_id)

    def get_image(self, scholar, query_id):
        image_link = self.get_any_from_attributes(scholar.attributes, ["claims", string_to_wikidata_key["image"], 0, "mainsnak", "datavalue", "value"], "image", query_id)
        return WIKIDATA_IMAGE + image_link.replace(" ", "_")
    
    def get_field(self, scholar, query_id):
        return self.get_any_from_attributes(scholar.attributes, ["claims", string_to_wikidata_key["field"], 0, "mainsnak", "datavalue", "value", "id"], "field", query_id)
       
    def get_advisors(self, scholar, query_id):
        advisors = list()
        for advisor in self.get_any_from_attributes(scholar.attributes, ["claims", string_to_wikidata_key["doctoral_advisor"]], "advisors", query_id):
            advisor_qid = self.get_any_from_attributes(advisor, ["mainsnak", "datavalue", "value", "id"], "advisor query ids", query_id)
            if advisor_qid:
                self.to_process.append(advisor_qid)
                advisors.append(advisor_qid)
        return advisors
    
    def get_students(self, scholar, query_id):
        students = list()
        
        for student in self.get_any_from_attributes(scholar.attributes, ["claims", string_to_wikidata_key["doctoral_student"]], "students", query_id):
            student_qid = self.get_any_from_attributes(student, ["mainsnak", "datavalue", "value", "id"], "student query id", query_id)
            if student_qid:
                self.to_process.append(student_qid)
                students.append(student_qid)
               
        return students

    def finish_and_print(self):
        self.scholar_json.write(json.dumps(
            self.all_scholars, indent=4, sort_keys=True))
        self.debug.close()
        self.scholar_json.close()


scholar_web = WikiDataScholars(max_scholars=5)
scholar_web.run()
