from bs4 import BeautifulSoup
import json
import urllib3
import certifi

http = urllib3.PoolManager(
  cert_reqs='CERT_REQUIRED',
  ca_certs=certifi.where()
)
res = http.request('GET', 'https://en.wikipedia.org/wiki/Isaac_Newton').data

soup = BeautifulSoup(res, 'html.parser')

def find_advisors_and_students(html_rows, cur_scholar):
  for row in html_rows:
    if row.findChildren(['th']):
      for th in row.findChildren('th'):
        print(th)
        str_array = []
        for string in th.strings:
          str_array.append(repr(string))
        complete_string = ''.join(str_array)
        complete_string.replace('\'', "")
        print(complete_string)
        if complete_string == "'Doctoral''advisor'" or "'Doctoral advisor'" == complete_string:
          get_links(row, "doctoral_advisors", cur_scholar)
        elif complete_string == "'Doctoral''students'":
          get_links(row, "doctoral_students", cur_scholar)
        elif complete_string == "'Academic''advisors'":
          get_links(row, "academic_advisors", cur_scholar)
        elif complete_string == "'Notable''students'":
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
        new_scholar = {'link': 'WIKI' + link, 'name': link[6:].replace("_", " ")}
        print(new_scholar)
        group_members.append(link_tag.attrs['title'])
  cur_scholar[group] = group_members


scholar = {'link': 'https://en.wikipedia.org/wiki/Albert_Einstein', 'name': 'Albert Einstein'}
sidebar_details_table = soup.findChildren('table')[0]
rows = sidebar_details_table.findChildren('tr')
print(find_advisors_and_students(rows, scholar))

