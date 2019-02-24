// set data file
scholar_data = "./george_scholars.json"

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

function dataLoadAndSetup() {
  d3.json(scholar_data, function(data) {
    scholars = data;
    console.log(scholars);
    setUpLinks();
    console.log(links);
  });
}

function findScholar(scholar) {
  let found_scholar = scholars.filter((doc) => {
    return doc.name === scholar["name"];
  });
  links.add({source: found_scholar, target: scholar});
}

function setUpLinks() {
  for (let i = 0; i < scholars.length; i++) {
    cur_scholar = scholars[i];
    for (let doc_advisor in cur_scholar["doctoral_advisors"]) {
      findScholar(doc_advisor);
    }
    for (let academic_advisor in cur_scholar["academic_advisors"]) {
      findScholar(academic_advisor);
    }
  }
}

dataLoadAndSetup();
console.log()