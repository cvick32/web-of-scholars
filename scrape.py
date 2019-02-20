from bs4 import BeautifulSoup

george = open('George_Akerlof.html', 'r')
div_only = open('div_only.html', 'w+')
div_only.seek(0)
div_only.truncate()

soup = BeautifulSoup(george.read(), 'html.parser')
sidebar_details_tag = soup.findAll("table", {"class": "infobox biography vcard"})

sidebar_details_table = soup.findChildren('table')[0]
rows = sidebar_details_table.findChildren('tr')

for row in rows: 
    if row.findChildren('th'):  
        for linebreak in row.find_all('br'):
            linebreak.extract()
        for th in row.findChildren('th'):
            print(th.string)
            print('---------------')


div_only.write(str(sidebar_details_tag))

div_only.close()




