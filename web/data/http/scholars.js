// set data file
scholar_data = "./data/http/after_http_fixes/prelim_fixed_scholars.json"

let scholars;
let links = [];
let totalLinks = 0;
let selectedScholar = null;

// set up canvas constants for D3
const width = 2000;
const height = 1000;
const color_set = ["#00C851", "#0099CC", "#ffeb3b", "#FF8800", "#ff4444"];
const colors = d3.scaleOrdinal(d3.schemeCategory10);

// negative repels objects, positive attracts
let forceStrength = -1000;
let circleSize = 13;

const svg = d3.select('body')
  .append('svg')
  .attr('oncontextmenu', 'return false;');

let defs = svg.append('svg:defs')

// define arrow in svg
defs.append('svg:marker')
  .attr('id', 'arrow')
  .attr('viewBox', '0 -5 10 10')
  .attr('refX', 6)
  .attr('markerWidth', 3)
  .attr('markerHeight', 3)
  .attr('orient', 'auto')
.append('svg:path')
  .attr('d', 'M0,-5L10,0L0,5')
  .attr('fill', '#000');


// set up container, path and circle objects
let container = svg.append('svg:g');
let path = container.append('svg:g').selectAll('path');
let circle = container.append('svg:g').selectAll('g');

// init D3 zoom
svg.call(d3.zoom()
  .scaleExtent([1 / 2, 8])
  .on('zoom', zoomed));

// init D3 force
const force = d3.forceSimulation()
  .force('link', d3.forceLink().id((d) => d.name).distance(150))
  .force('charge', d3.forceManyBody().strength(forceStrength))
  .force('x', d3.forceX(width / 2))
  .force('y', d3.forceY(height / 2))
  .on('tick', tick);

/**
 * function called on zoom event
 */
function zoomed() {
  container.attr("transform", d3.event.transform);
}

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
    setUpImages();
    setSVG();
  });
}

/**
 * constructs links between related scholars
 */
function setUpLinks() {
  for (let i = 0; i < scholars.length; i++) {
    cur_scholar = scholars[i];
    doctoral_advisors = cur_scholar["doctoral_advisors"];
    academic_advisors = cur_scholar["academic_advisors"];
    if (doctoral_advisors) {
      for (let i = 0; i < doctoral_advisors.length; i++) {
        findAdvisor(cur_scholar, doctoral_advisors[i]);
      }
    }
    if (academic_advisors) {
      for (let i = 0; i < academic_advisors.length; i++) {
        findAdvisor(cur_scholar, academic_advisors[i]);
      }
    }
  }
}

/**
 * extracts image of each scholar and adds it to the
 * svg definitions
 */
function setUpImages() {
  for (let i = 0; i < scholars.length; i++) {
    cur_scholar = scholars[i]
    cur_scholar_image = cur_scholar["image"];
    cur_scholar_name = cur_scholar["name"];
    if (cur_scholar_image) {
      defs
      .append('svg:pattern')
        .attr('id', cur_scholar_name.replace(" ", "_") + '_image')
        .attr('width', '100%')
        .attr('height', '100%')
      .append('svg:image')
        .attr('x', 0)
        .attr('y', 0)
        .attr('xlink:href', cur_scholar_image)
    }
  }
}

/**
 * finds a given scholar's advisor
 * @param {scholar object} scholar 
 * @param {string} advisor_name 
 */
function findAdvisor(scholar, advisor_name) {
  let found_advisor = scholars.filter((doc) => {
    return doc.name === advisor_name;
  });
  if (found_advisor[0]) {
    links.push({source: found_advisor[0], target: scholar, left: false, right: true});
  }
}

/**
 *  d3 function that happens each clock tick
 */
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

/**
 * sets the svg objects for all scholars and links
 */
function setSVG() {
  path = path.data(links);
  path.exit().remove();

  path = path.enter().append('svg:path')
    .attr('class', 'link')
    .style('marker', (d) => 'url(#arrow')
    .merge(path);

  circle = circle.data(scholars, (d) => d.name);

  circle.exit().remove();

  const g = circle.enter().append('svg:g');

  g.append('svg:circle')
    .attr('class', 'node')
    .attr('r', circleSize)
    .style('fill', (d) => determineInfluence(d))
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

function determineInfluence(scholar) {
  if (scholar.doctoral_students) {
    let num_students = scholar.doctoral_students.length;
    if (num_students > 5) {
      return "#CCAC00"; // gold
    } else {
      return color_set[num_students - 1];
    }
  } else {
    return "#ffe4c4";
  }
}

// app start
dataLoadAndSetup();