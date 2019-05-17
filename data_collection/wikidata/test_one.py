import json
from wikidata.client import Client

check = open("debug.json", "w+")
check.seek(0)
check.truncate()
client = Client()
scholar = client.get("Q222541")

check.write(json.dumps(scholar.attributes, indent=4, sort_keys=True))
