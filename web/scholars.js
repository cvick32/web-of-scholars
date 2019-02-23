// set up SVG for D3
const width = 960;
const height = 500;

const svg = d3.select('body')
  .append('svg')
  .attr('oncontextmenu', 'return false;')
  .attr('width', width)
  .attr('height', height);

let scholars;
const links = new Set([]);

async function dataLoadAndSetup() {
  d3.json("./scholars.json", function(data) {
    scholars = data;
    setUpLinks();
  });
}

function findScholar(scholar) {
  let found_scholar = scholars.filter((doc) => {
    return doc.name === scholar["name"];
  });
  links.push({source: found_scholar, target: scholar});
}

function setUpLinks() {

  console.log('adsf');
  for (const scholar in scholars) {
    console.log('adsf');
    for (const doc_advisor in scholar["doctoral_advisors"]) {
      findScholar(doc_advisor);
    }
    for (const academic_advisor in scholar["academic_advisors"]) {
      findScholar(academic_advisor);
    }
  }
}

dataLoadAndSetup();