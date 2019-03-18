import json
from wikidata import Client

check = open('debug.json', 'w+')
check.seek(0)
check.truncate()
client = Client()
george = client.get('Q222541')

property_map = {
  'doctoral_advisor':'P184',
  'doctoral_student':'P184',
  'student':'P802',
  'field':'P101',
  'image':'P18'
}

check.write(json.dumps(george.attributes, indent=4, sort_keys=True))

doc_advisor = george.attributes['claims'][property_map['doctoral_advisor']][0]['mainsnak']['datavalue']['value']['id']
print(doc_advisor)


class WikiDataScholars:
  def __init__(self):
     # open necessary files
    self.debug = open('debug.txt', "w+")
    self.debug.seek(0)
    self.debug.truncate()

    self.output = open('output.txt', "w+")
    self.output.seek(0)
    self.output.truncate()

    self.scholar_json = open('scholars.json', "w+")
    self.scholar_json.seek(0)
    self.scholar_json.truncate()
    # set arbitrary limit and scholars for now
    self.Wiki_Client = Client()
    
    self.to_process = ["Q22541"]
    self.seen_scholars = set()
    self.all_scholars = list()
  
  def run(self):
    while self.to_process:
      self.get_scholar_advisors_and_students(self.to_process[0])
      self.to_process = self.to_process[:1]
    self.finish_and_print()
  
  def get_scholar_advisors_and_students(self, scholar_query_id):
    cur_scholar = self.Wiki_Client(scholar_query_id)
    cur_scholar_json = {
      'name':cur_scholar.attributes['aliases']['en'][0]['value'],
      'image':cur_scholar.attributes['sitelinks']['en']['url'],
      'link':cur_scholar.attributes['sitelinks']['en']['url'],
      'doctoral_advisor':list(),
      'doctoral_student':list(),
    }
    # get scholar advisors
    for advisor in cur_scholar.attributes['claims'][property_map['doctoral_advisor']]:
      self.to_process.append(advisor['mainsnak']['datavalue']['value']['id'])
    
    # get scholar students
    for student in cur_scholar.attributes['claims'][property_map['doctoral_student']]:
      self.to_process.append(student['mainsnak']['datavalue']['value']['id'])
    


    self.seen_scholars.add()
    self.all_scholars.append(cur_scholar)

  def finish_and_print(self):
    return