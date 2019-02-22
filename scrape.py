from bs4 import BeautifulSoup
import json
import urllib3
import certifi

WIKI = "https://en.wikipedia.org"
http = urllib3.PoolManager(
  cert_reqs='CERT_REQUIRED',
  ca_certs=certifi.where()
)

debug = open('debug.txt', "w+")
debug.seek(0)
debug.truncate()

'''
  json schema for scholars 
  { 
    name: string;
    image: string;
    advisors: [string];
    students: [string];
    link: string
  }
'''

george_json = {
  'link': 'https://en.wikipedia.org/wiki/George_Akerlof',
  'name': 'George Akerlof'
}

albert_json = {
  'link': 'https://en.wikipedia.org/wiki/Albert_Einstein',
  'name': 'Albert Einstein'
}

isaac_json = {
  'link': 'https://en.wikipedia.org/wiki/Isaac_Newton',
  'name': 'Isaac Newton'
}

paul_json = {
  'link': 'https://en.wikipedia.org/wiki/Paul_Erd%C5%91s',
  'name': 'Paul Erdős'
}

marie_json ={
  'link': 'https://en.wikipedia.org/wiki/Marie_Curie',
  'name': 'Marie Curie'
}

to_process = [albert_json, george_json, isaac_json, marie_json, paul_json]

seen_scholars = set()

all_scholars = list()

def make_request(scholar):
  if not scholar['name'] in seen_scholars:
    res = http.request('GET', scholar['link']).data
    soup = BeautifulSoup(res, 'html.parser')
    try:
      sidebar_details_table = soup.findChildren('table')[0]
    except:
      print('no info table')
      return 
    rows = sidebar_details_table.findChildren('tr')
    all_scholars.append(find_advisors_and_students(rows, scholar))
    seen_scholars.add(scholar['name'])
  

def find_advisors_and_students(html_rows, cur_scholar):
  for row in html_rows:
    if row.findChildren(['th']):
      for th in row.findChildren('th'):
        str_array = []
        for string in th.strings:
          str_array.append(repr(string))
        complete_string = ''.join(str_array)
        if complete_string == "'Doctoral''advisor'" or complete_string == "'Doctoral advisor'":
          get_links(row, "doctoral_advisors", cur_scholar)
        elif complete_string == "'Doctoral''students'" or complete_string == "'Doctoral students'":
          get_links(row, "doctoral_students", cur_scholar)
        elif complete_string == "'Academic''advisors'" or complete_string == "'Academic advisors'":
          get_links(row, "academic_advisors", cur_scholar)
        elif complete_string == "'Notable''students'" or complete_string == "'Academic advisors'":
          get_links(row, "notable_students", cur_scholar)
    else:
      if row.findChildren('img'):
        cur_scholar["image"] = 'https:/' + row.findChildren('img')[0].attrs['src']
  return cur_scholar

def get_links(cur_row, group, cur_scholar):
  link_tags = cur_row.findChildren('a')
  group_members = []
  for link_tag in link_tags:
    if link_tag.attrs['href']:
      link = link_tag.attrs['href']
      if link[:6] == '/wiki/':
        new_scholar_name = link[6:].replace("_", " ")
        new_scholar = {'link': WIKI + link, 'name': new_scholar_name }
        to_process.append(new_scholar)
        group_members.append(new_scholar_name)
  cur_scholar[group] = group_members


while to_process:
  make_request(to_process[0])
  to_process = to_process[1:]

debug.write("full JSON of all found scholars\n")
debug.write(json.dumps(all_scholars, indent=4, sort_keys=True))
debug.write("\nnames of all found scholars\n")
for scholar in seen_scholars:
  debug.write(scholar + ",\n")
debug.write('number of found scholars in JSON array: ')
debug.write(str(len(seen_scholars)) + '\n')
debug.write('number of found scholars in scholars_seen set: ')
debug.write(str(len(all_scholars)))

debug.close()