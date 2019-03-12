# Web of Scholars :mortar_board:

## Purpose
I made this so I could see the relationships between scholars that I had been looking up. An interesting byproduct of this web is that 
you get to see which scholar influenced others. 
## Viewing 
Right now you can view a truncated version of the web that shows the first 300 links `data_collection/scrape.py` found for [Mathias Dewatripont](https://en.wikipedia.org/wiki/Mathias_Dewatripont), link to the site above. It runs super hot right now and it will probably be stressful for slower computers to run for even a few minutes. Sorry about that, I'm working on a better solution.
## Notes
- should this be a lookup where you search someone and then you see their tree?
- maybe it should be a tool for people on wikipedia to see which important links need more information
  - this will obviously take a while but I think it would be cool to be able to see that someones doctoral student doesn't have a lot of info and fill it in
- want to split everyone up by field, but not every entry has a field  

## Roadmap
- [ ] Single view  
- [ ] Full view  
- [ ] Roll over to see wikipedia entry  
- [ ] Scaling of circles from a slider
- [x] Get all possible wiki entries available from Akerlof
- [x] Get all possible wiki entries for set of scholars
- [x] Display scholars as a directed graph
- [x] Implement zoom in to graph, i know y'all wanted it :eyes:
- [x] Make image from wikipedia page the show up in circle
- [ ] Make image from wikipedia page not look terrible in circle
- [x] Scaling colors by number of connections (influenceColor) put back in images
- [ ] Scaling size by number of connections (influenceSize)
- [ ] Need to fix scraping to not get Doctoral Advisor entries
