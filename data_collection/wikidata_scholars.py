import json
from wikidata.client import Client

string_to_wikidata_key = {
    "doctoral_advisor": "P184",
    "doctoral_student": "P185",
    "field": "P101",
    "image": "P18",
}

'''
This is a map from names of attributes to the list of attributes
that are needed to call on a list of attributes to get the desired
field. Let's try an example:

Scholar 101 = {
    "claims": ...
    "aliases": {
        "en": [{"value": "Cole Vick"}, "]
        "es": ...
        ...
    }
    ...
}

So to get the correct name out of this structure we need to navigate 
to the `aliases` object, then select english as the language, then 
select the first position of the array, then select the value of that
object. So, it would be exactly the array described below to find the 
name, if we iterate over the attributes, as we do in the function
`get_value_from_attributes` below.
'''
name_to_attribute = {
    "advisors": ["claims", string_to_wikidata_key["doctoral_advisor"]],
    "field": ["claims", string_to_wikidata_key["field"], 0, "mainsnak", "datavalue", "value", "id"],
    "image": ["claims", string_to_wikidata_key["image"], 0, "mainsnak", "datavalue", "value"],
    "name": ["aliases", "en", 0, "value"],
    "other_name": ["aliases", "en", "value"],
    "title_name": ["labels", "en", "value"],
    "scholar_qid": ["mainsnak", "datavalue", "value", "id"],
    "students": ["claims", string_to_wikidata_key["doctoral_student"]],
    "wiki_link": ["sitelinks", "enwiki", "url"]
}

WIKIDATA_IMAGE = "https://commons.wikimedia.org/wiki/File:"

class WikiDataScholars:
    def __init__(self, max_scholars, starting_scholars=["Q222541"], scholar_json_file="scholars.json", debug_file="debug.txt"):
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

        self.num_processed = 0

    def run(self):
        """Begin the scraping process for the web."""
        while self.to_process:
            if self.num_processed >= self.max_scholars:
                break
            if not self.to_process[0] in self.seen_scholars:
                self.seen_scholars.add(self.to_process[0])
                self.get_scholar_advisors_and_students(self.to_process[0])
            self.to_process = self.to_process[1:]
            self.num_processed += 1
        self.finish_and_print()

    def get_scholar_advisors_and_students(self, scholar_query_id):
        self.cur_scholar_id = scholar_query_id

        cur_scholar = self.Wiki_Client.get(scholar_query_id)

        scholar_name      = self.get_name(cur_scholar)
        scholar_wiki_link = self.get_wiki_link(cur_scholar)
        scholar_image     = self.get_image(cur_scholar)
        scholar_field     = self.get_field(cur_scholar)
        scholar_advisors  = self.get_advisors(cur_scholar)
        scholar_students  = self.get_students(cur_scholar)

        self.debug.write(f"Scholar Name: {scholar_name}\n")
        self.debug.write(f"Scholar Query ID: {scholar_query_id}\n")
        print("Current Scholar: {} {}".format(scholar_name, scholar_query_id))
      
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
        image_link = self.get_value_from_attributes("image", scholar.attributes)
        return WIKIDATA_IMAGE + image_link.replace(" ", "_")
    
    def get_field(self, scholar):
        return self.get_value_from_attributes("field", scholar.attributes)
       
    def get_advisors(self, scholar):
        advisors = list()
        for advisor in self.get_value_from_attributes("advisors", scholar.attributes):
            advisor_qid = self.get_value_from_attributes("scholar_qid", advisor)
            if advisor_qid:
                self.to_process.append(advisor_qid)
                advisors.append(advisor_qid)
        return advisors
    
    def get_students(self, scholar):
        students = list()
        for student in self.get_value_from_attributes("students", scholar.attributes):
            student_qid = self.get_value_from_attributes("scholar_qid", student)
            if student_qid:
                self.to_process.append(student_qid)
                students.append(student_qid)
        return students

    def finish_and_print(self):
        self.scholar_json.write(json.dumps(
            self.all_scholars, indent=4, sort_keys=True))
        self.debug.close()
        self.scholar_json.close()


scholar_web = WikiDataScholars(max_scholars=10)
scholar_web.run()
