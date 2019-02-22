from bs4 import BeautifulSoup
import json
import urllib3
import certifi

WIKI = "https://en.wikipedia.org"
http = urllib3.PoolManager(
  cert_reqs='CERT_REQUIRED',
  ca_certs=certifi.where()
)

george_json = {
  'link': 'https://en.wikipedia.org/wiki/George_Akerlof',
  'name': 'George Akerlof'
}

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

to_process = [george_json]

all_scholars = []

def make_request(scholar):
  res = http.request('GET', scholar['link']).data
  soup = BeautifulSoup(res, 'html.parser')
  sidebar_details_table = soup.findChildren('table')[0]
  rows = sidebar_details_table.findChildren('tr')
  all_scholars.append(find_advisors_and_students(rows, scholar))

def find_advisors_and_students(html_rows, cur_scholar):
  for row in html_rows:
    if row.findChildren(['th']):
      for th in row.findChildren('th'):
        str_array = []
        for string in th.strings:
          str_array.append(repr(string))
        complete_string = ''.join(str_array)
        if complete_string == "'Doctoral''advisor'":
          get_links(row, "advisors", cur_scholar)
        elif complete_string == "'Doctoral''students'":
          get_links(row, "students", cur_scholar)
    else:
      if row.findChildren('img'):
        cur_scholar["image"] = WIKI + row.findChildren('img')[0].attrs['src']
  
  return cur_scholar

def get_links(cur_row, group, cur_scholar):
  link_tags = cur_row.findChildren('a')
  group_members = []
  for link_tag in link_tags:
    if link_tag.attrs['href']:
      link = link_tag.attrs['href']
      if link[:6] == '/wiki/':
        new_scholar = {'link': WIKI + link, 'name': link[6:].replace("_", " ")}
        to_process.append(new_scholar)
        group_members.append(link_tag.attrs['title'])
  cur_scholar[group] = group_members

make_request(george_json)

counter = 0
while to_process and counter < 100:
  print(to_process[0])
  make_request(to_process[0])
  to_process = to_process[1:]
  counter += 1


print(all_scholars)