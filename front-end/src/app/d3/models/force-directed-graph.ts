import { EventEmitter } from '@angular/core';
import { Link } from './link';
import { Node } from './node';
import * as d3 from 'd3';

const FORCES = {
  LINKS: 1 / 50,
  COLLISION: 1,
  CHARGE: -100
};

export class ForceDirectedGraph {
  public ticker: EventEmitter<d3.Simulation<Node, Link>> = new EventEmitter();
  public simulation: d3.Simulation<any, any>;

  private nodes: Node[] = [];
  private links: Link[] = [];

  constructor(nodes: Node[], links: Link[], options: { width, height}) {
    this.nodes = nodes;
    this.links = links;

    if (!options || !options.width || !options.height) {
      throw new Error('missing options when initializing simulation');
    }
     this.initSimulation(options);
  }

  initSimulation(options) {
    if (!this.simulation) {
      const ticker = this.ticker;

      this.simulation = d3.forceSimulation().force('charge', d3.forceManyBody().strength(FORCES.CHARGE));
      this.simulation.on('tick', () => ticker.emit(this.simulation));
      this.initNodes();
      this.initLinks();
    }

    this.simulation.force('centers', d3.forceCenter(options.width / 2, options.height / 2));
    this.simulation.restart();
  }

  private initNodes() {
    this.simulation.nodes(this.nodes);
  }

  private initLinks() {
    this.simulation.force('links', d3.forceLink(this.links).id(d => d['id']).strength(FORCES.LINKS));
  }

  connectNodes(source, target) {
    let link;

    if (!this.nodes[source] || !this.nodes[target]) {
      throw new Error('One of the nodes does not exist');
    }

    link = new Link(source, target);
    this.simulation.stop();
    this.links.push(link);
    this.simulation.alphaTarget(0.3).restart();

    this.initLinks();
  }
}
