from data_collection.wikidata_scholars import WikiDataScholars

"""
run `python3 generater_scholars.py` to have a servable scholars.json
change max_scholars to have more or fewer scholars
"""

wd = WikiDataScholars(max_scholars=50)
wd.run()