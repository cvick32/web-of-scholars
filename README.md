# Web of Scholars :mortar_board:

## Purpose
I made this so I could see the relationships between scholars that I had been looking up. An interesting byproduct of this web is that 
you get to see which scholars influenced other scholars. 
## Viewing 
Right now you can view a truncated version of the web that shows the first 300 links `data_collection/scrape.py` found for [Mathias Dewatripont](https://en.wikipedia.org/wiki/Mathias_Dewatripont), link to the site above. It runs super hot right now and it will probably be stressful for slower computers to run for even a few minutes. Sorry about that, I'm working on a better solution.
## Notes
- should this be a lookup where you search someone and then you see their tree?
- maybe it should be a tool for people on wikipedia to see which important links need more information
  - this will obviously take a while but I think it would be cool to be able to see that someones doctoral student doesn't have a lot of info and fill it in
- want to split everyone up by field, but not every entry has a field  
- need to look at [neo4j](https://neo4j.com/developer/)
- this could also be an auto-posting instagram page
  - first slide is the WoS graph between a scholar and their connections
  - second slide is their photo
  - caption is their first paragraph from wikipedia

## Local Running
`cd data_collection`
`python3 -m venv scholar`
`. scholar/bin/activate`
`pip install -r requirements.txt`
`export FLASK_APP=app.py`
`flask run`
`cd ..`
`cd front-end`
`ng serve`

## Roadmap
- [ ] Actually launch
### Front-end
- [x] Single view  
- [x] Full view  
- [ ] Roll over to see wikipedia entry  
- [ ] Scaling of circles from a slider
- [x] Scaling size by number of connections 
- [ ] Make image from wikipedia page not look terrible in circle
- [x] Switch to Angular 9
- [x] Display scholars as a graph
- [x] Implement zoom in to graph, i know y'all wanted it :eyes:
- [x] Make image from wikipedia page the show up in circle
- [x] Scaling colors by number of connections (influenceColor) put back in images
- [ ] Add route for coauthors + publications
### Back-end
- [ ] Need to fix scraping to not get Doctoral Advisor entries
- [ ] Add another route for viewing coauthors + publications 
- [x] Refactor scraping
- [x] NEED TO LOOK AT WIKIDATA
- [x] Get all possible wiki entries available from Akerlof
- [x] Get all possible wiki entries for set of scholars
