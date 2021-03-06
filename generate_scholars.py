from data_collection.wikidata_scholars import WikiDataScholars

"""
run `python3 generater_scholars.py` to have a servable scholars.json
change max_scholars to have more or fewer scholars
"""

wd = WikiDataScholars(scholar_json_file="data_collection/scholars.json")
scholars = wd.run(max_scholars=200)
wd.finish_and_print(scholars)
