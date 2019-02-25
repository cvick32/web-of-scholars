// set data file
scholar_data = "./data/squeezed_scholars.json"

let scholars;
let links = [];
let totalLinks = 0;

/**
 * Ansync method provided by D3 for reading in JSON data.
 * After we grab the data from the file, we set up the link
 * data structure that we will use for graphically rendering
 * the web.
 */
function dataLoadAndSetup() {
  d3.json(scholar_data).then(function(data) {
    scholars = data;
    setUpLinks();
    restart();
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
    if (academic_advisors) {
      for (let i = 0; i < academic_advisors.length; i++) {
        findScholar(academic_advisors[i], cur_scholar);
      }
    }
  }
}

function findScholar(advisor_name, scholar) {
  let found_advisor = scholars.filter((doc) => {
    return doc.name === advisor_name;
  });
  if (found_advisor[0]) {
    links.push({source: found_advisor[0], target: scholar, left: false, right: true});
  }
}


// set up SVG for D3
const width = 2000;
const height = 1000;
const colors = d3.scaleOrdinal(d3.schemeCategory10);


test_links = [
  { source: {
    "doctoral_advisors": [
        "Robert Solow"
    ],
    "doctoral_students": [
        "Charles Engel",
        "Adriana Kugler"
    ],
    "image": "https:///upload.wikimedia.org/wikipedia/commons/thumb/1/18/George_Akerlof.jpg/225px-George_Akerlof.jpg",
    "link": "https://en.wikipedia.org/wiki/George_Akerlof",
    "name": "George Akerlof"
  }, target: {
    "doctoral_advisors": [
        "Jeffrey Frankel",
        "George Akerlof",
        "Janet Yellen"
    ],
    "link": "https://en.wikipedia.org/wiki/Charles_Engel",
    "name": "Charles Engel"
  }, left: false, right: true }
]

const svg = d3.select('body')
  .append('svg')
  .attr('oncontextmenu', 'return false;')
  .attr('width', width)
  .attr('height', height);

// set up path and circle objects
let path = svg.append('svg:g').selectAll('path');
let circle = svg.append('svg:g').selectAll('g');

// init D3 zoom
svg.call(d3.zoom()
  .scaleExtent([1 / 2, 8])
  .on('zoom', zoomed));

function zoomed() {
  path.attr("transform", d3.event.transform);
  circle.attr("transform", d3.event.transform);
}

// init D3 force
const force = d3.forceSimulation()
  .force('link', d3.forceLink().id((d) => d.name).distance(150))
  .force('charge', d3.forceManyBody().strength(-500))
  .force('x', d3.forceX(width / 2))
  .force('y', d3.forceY(height / 2))
  .on('tick', tick);

svg.append('svg:defs').append('svg:marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 6)
    .attr('markerWidth', 3)
    .attr('markerHeight', 3)
    .attr('orient', 'auto')
  .append('svg:path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#000');

let selectedScholar = null;

function tick() {
  path.attr('d', (d) => {
    const deltaX  = d.target.x - d.source.x;
    const deltaY  = d.target.y - d.source.y;
    const dist    = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
    const normX   = deltaX / dist;
    const normY   = deltaY / dist;
    const sourcePadding = d.left ? 17 : 12;
    const targetPadding = d.right ? 17 : 12;
    const sourceX = d.source.x + (sourcePadding * normX);
    const sourceY = d.source.y + (sourcePadding * normY);
    const targetX = d.target.x - (targetPadding * normX);
    const targetY = d.target.y - (targetPadding * normY);
  
    return `M${sourceX},${sourceY}L${targetX},${targetY}`;
  });
  circle.attr('transform', (d) => `translate(${d.x},${d.y})`);
}

function restart() {
  path = path.data(links);
  path.exit().remove();

  path = path.enter().append('svg:path')
    .attr('class', 'link')
    .style('marker', (d) => 'url(#arrow')
    .merge(path);

  circle = circle.data(scholars, (d) => d.name);

  circle.selectAll('circle')
    .style('fill', (d) => colors(d.name));

  circle.exit().remove();

  const g = circle.enter().append('svg:g');

  g.append('svg:circle')
    .attr('class', 'node')
    .attr('r', 12)
    .style('fill', colors(0))
    .style('stroke', d3.rgb(colors(0)).darker().toString());
  
  g.append('svg:text')
    .attr('x', 0)
    .attr('y', 4)
    .attr('class', 'name')
    .text((d) => d.name);
  
  circle = g.merge(circle);


  force.nodes(scholars).force('link').links(links);

  force.alphaTarget(0.3).restart();

}

// app start
dataLoadAndSetup();