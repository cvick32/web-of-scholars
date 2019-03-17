from wikidata.client import Client 
import json

check = open('debug.json', 'w+')
check.seek(0)
check.truncate()
client = Client()
george = client.get('Q222541')

check.write(json.dumps(george.attributes, indent=4, sort_keys=True))

