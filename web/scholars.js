// set data file
scholar_data = "./data/squeezed_scholars.json"

// set up SVG for D3
const width = 960;
const height = 500;

const svg = d3.select('body')
  .append('svg')
  .attr('oncontextmenu', 'return false;')
  .attr('width', width)
  .attr('height', height);

let scholars;
const links = new Set();

/**
 * Ansync method provided by D3 for reading in JSON data.
 * After we grab the data from the file, we set up the link
 * data structure that we will use for graphically rendering
 * the web.
 */
function dataLoadAndSetup() {
  d3.json(scholar_data, function(data) {
    scholars = data;
    setUpLinks();
    console.log(links);
  });
}

function setUpLinks() {
  for (let i = 0; i < scholars.length; i++) {
    cur_scholar = scholars[i];
    doctoral_advisors = cur_scholar["doctoral_advisors"];
    academic_advisors = cur_scholar["academic_advisors"];

    if (doctoral_advisors) {
      for (let i = 0; i < doctoral_advisors.length; i++) {
        findScholar(doctoral_advisors[i], cur_scholar);
      }
    }
    if (academic_advisors)
    for (let i = 0; i < academic_advisors.length; i++) {
      findScholar(academic_advisors[i], cur_scholar);
    }
  }
}

function findScholar(advisor_name, scholar) {
  let found_advisor = scholars.filter((doc) => {
    return doc.name === advisor_name;
  });
  links.add({source: found_advisor, target: scholar});
}



// app start
dataLoadAndSetup();