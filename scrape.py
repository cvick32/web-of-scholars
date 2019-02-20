from bs4 import BeautifulSoup

george = open('George_Akerlof.html', 'r')
div_only = open('div_only.html', 'w+')
div_only.seek(0)
div_only.truncate()

soup = BeautifulSoup(george.read(), 'html.parser')

sidebar_details_tag = soup.findAll("table", {"class": "infobox biography vcard"})

div_only.write(str(sidebar_details_tag))



div_only.close()




