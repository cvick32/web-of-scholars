from bs4 import BeautifulSoup
import json

george = open('George_Akerlof.html', 'r')

wiki = "https://en.wikipedia.org"
soup = BeautifulSoup(george.read(), 'html.parser')
advisor_soup = BeautifulSoup(
    '''<th scope="row">Doctoraladvisor</th>''', 'html.parser')
student_soup = BeautifulSoup(
    '''<th scope="row">Doctoralstudents</th>''', 'html.parser')
sidebar_details_tag = soup.findAll(
    "table", {"class": "infobox biography vcard"})

sidebar_details_table = soup.findChildren('table')[0]
rows = sidebar_details_table.findChildren('tr')

george_json = {}

to_process = []

def findAdvisorsAndStudents(htmlRows):
  for row in htmlRows:
    if row.findChildren(['th']):
      for th in row.findChildren('th'):
        str_array = []
        for string in th.strings:
          str_array.append(repr(string))
        complete_string = ''.join(str_array)
        complete_string.replace("'", "")

        if complete_string == "'Doctoral''advisor'":
          link_tags = row.findChildren('a')
          doc_advisors = []
          for link_tag in link_tags:
            if link_tag.attrs['href']:
              link = link_tag.attrs['href']
              if link[:6] == '/wiki/':
                to_process.append(wiki + link)
                doc_advisors.append(link_tag.attrs['title'])
          george_json["advisors"] = doc_advisors
        elif complete_string == "'Doctoral''students'":
          link_tags = row.findChildren('a')
          doc_students = []
          for link_tag in link_tags:
            if link_tag.attrs['href']:
              link = link_tag.attrs['href']
              if link[:6] == '/wiki/':
                to_process.append(wiki + link)
                doc_students.append(link_tag.attrs['title'])
          george_json["students"] = doc_students

findAdvisorsAndStudents(rows)

print(george_json)
print(to_process)