from bs4 import BeautifulSoup
import json
import urllib3
import certifi

WIKI = "https://en.wikipedia.org"
http = urllib3.PoolManager(
  cert_reqs='CERT_REQUIRED',
  ca_certs=certifi.where()
)

george_json = {}

to_process = []
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
def make_request(link):
  res = http.request('GET', link).data
  soup = BeautifulSoup(res, 'html.parser')
  sidebar_details_table = soup.findChildren('table')[0]
  rows = sidebar_details_table.findChildren('tr')
  cur_scholar = {}
  find_advisors_and_students(rows)


def find_advisors_and_students(html_rows):
  for row in html_rows:
    if row.findChildren(['th']):
      for th in row.findChildren('th'):
        str_array = []
        for string in th.strings:
          str_array.append(repr(string))
        complete_string = ''.join(str_array)
        if complete_string == "'Doctoral''advisor'":
          get_links(row, "advisors")
        elif complete_string == "'Doctoral''students'":
          get_links(row, "students")
    else:
      if row.findChildren('img'):
        george_json["image"] = WIKI + row.findChildren('img')[0].attrs['src']

def get_links(cur_row, group):
  link_tags = cur_row.findChildren('a')
  group_members = []
  for link_tag in link_tags:
    if link_tag.attrs['href']:
      link = link_tag.attrs['href']
      if link[:6] == '/wiki/':
        new_scholar = {'link': WIKI + link, 'name': link[6:].replace("_", " ")}
        to_process.append(new_scholar)
        group_members.append(link_tag.attrs['title'])
  george_json[group] = group_members

make_request('https://en.wikipedia.org/wiki/George_Akerlof')

print(george_json)
print(to_process)