from bs4 import BeautifulSoup
import json
import urllib3
import certifi

WIKI = "https://en.wikipedia.org"
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

"""
  json schema for scholars 
  { 
    name: string;
    image: string;
    advisors: [string];
    students: [string];
    link: string
  }
"""

george_json = {
    "link": "https://en.wikipedia.org/wiki/George_Akerlof",
    "name": "George Akerlof",
}

albert_json = {
    "link": "https://en.wikipedia.org/wiki/Albert_Einstein",
    "name": "Albert Einstein",
}

isaac_json = {
    "link": "https://en.wikipedia.org/wiki/Isaac_Newton",
    "name": "Isaac Newton",
}

paul_json = {
    "link": "https://en.wikipedia.org/wiki/Paul_Erd%C5%91s",
    "name": "Paul Erdős",
}

marie_json = {
    "link": "https://en.wikipedia.org/wiki/Marie_Curie",
    "name": "Marie Curie",
}

mathias_json = {
    "link": "https://en.wikipedia.org/wiki/Mathias_Dewatripont",
    "name": "Mathias Dewatripont",
}

# ~3k results
# to_process = [albert_json, george_json, isaac_json, marie_json, paul_json]

# ~3k results
# to_process = [george_json]
# Turns out if you add checks for academic advisors and non-single-quote
#   you get 3k no matter what with george


class ScholarWeb:
    def __init__(self):
        # open necessary files
        self.debug = open("debug.txt", "w+")
        self.debug.seek(0)
        self.debug.truncate()

        self.output = open("output.txt", "w+")
        self.output.seek(0)
        self.output.truncate()

        self.scholar_json = open("scholars.json", "w+")
        self.scholar_json.seek(0)
        self.scholar_json.truncate()
        # set arbitrary limit and scholars for now
        self.total_scholars = 300
        self.no_infobox = 0

        # self.to_process = [albert_json, george_json, isaac_json, marie_json, paul_json]
        self.to_process = [mathias_json]
        self.seen_scholars = set()
        self.all_scholars = list()

    def make_request(self, scholar):
        if not scholar["name"] in self.seen_scholars:
            res = http.request("GET", scholar["link"]).data
            soup = BeautifulSoup(res, "html.parser")
            try:
                sidebar_details_table = soup.find(class_="infobox biography vcard")
                if sidebar_details_table is None:
                    sidebar_details_table = soup.find(class_="infobox vcard")
                    if sidebar_details_table is None:
                        self.no_infobox += 1
                        raise ValueError(scholar["name"] + " has no infobox attribute")
            except ValueError as err:
                self.debug.write(repr(err) + "\n")
                return
            print(scholar)
            rows = sidebar_details_table.find_all("tr")
            self.all_scholars.append(self.find_advisors_and_students(rows, scholar))
            self.seen_scholars.add(scholar["name"])

    def find_advisors_and_students(self, html_rows, cur_scholar):
        for row in html_rows:
            if row.findChildren(["th"]):
                for th in row.findChildren("th"):
                    str_array = []
                    for string in th.strings:
                        str_array.append(repr(string))
                        complete_string = "".join(str_array)
                        if (
                            complete_string == "'Doctoral''advisor'"
                            or complete_string == "'Doctoral advisor'"
                        ):
                            self.get_links(row, "doctoral_advisors", cur_scholar)
                        elif (
                            complete_string == "'Doctoral''students'"
                            or complete_string == "'Doctoral students'"
                        ):
                            self.get_links(row, "doctoral_students", cur_scholar)
                        elif (
                            complete_string == "'Academic''advisors'"
                            or complete_string == "'Academic advisors'"
                        ):
                            self.get_links(row, "academic_advisors", cur_scholar)
                        elif (
                            complete_string == "'Notable''students'"
                            or complete_string == "'Academic advisors'"
                        ):
                            self.get_links(row, "notable_students", cur_scholar)
            else:
                if row.findChildren("img"):
                    cur_scholar["image"] = (
                        "https:/" + row.findChildren("img")[0].attrs["src"]
                    )
        return cur_scholar

    def get_links(self, cur_row, group, cur_scholar):
        link_tags = cur_row.findChildren("a")
        group_members = []
        for link_tag in link_tags:
            if link_tag.attrs["href"]:
                link = link_tag.attrs["href"]
                if (
                    link[:6] == "/wiki/"
                    and not link == "https://en.wikipedia.org/wiki/Doctoral_advisor"
                ):
                    new_scholar_name = link[6:].replace("_", " ")
                    new_scholar = {"link": WIKI + link, "name": new_scholar_name}
                    self.to_process.append(new_scholar)
                    group_members.append(new_scholar_name)
        cur_scholar[group] = group_members

    def finish_and_print(self):
        self.scholar_json.write(json.dumps(self.all_scholars, indent=4, sort_keys=True))
        self.output.write("names of all found scholars\n")
        for scholar in self.seen_scholars:
            self.output.write(scholar + ",\n")
        self.output.write("number of found scholars in JSON array: ")
        self.output.write(str(len(self.seen_scholars)) + "\n")
        self.output.write("number of found scholars in scholars_seen set: ")
        self.output.write(str(len(self.all_scholars)))

        self.debug.write("number of scholars with no infobox: " + str(self.no_infobox))
        self.debug.close()
        self.output.close()
        self.scholar_json.close()

    def run(self):
        while self.to_process:
            if len(self.seen_scholars) < self.total_scholars:
                self.make_request(self.to_process[0])
                self.to_process = self.to_process[1:]
            else:
                self.finish_and_print()
                break

scholar_web = ScholarWeb()
scholar_web.run()