import { Node } from './';

export class Link implements d3.SimulationLinkDatum<Node> {

  index?: number;

  source: Node;
  target: Node;

  constructor(source, target) {
    this.source = source;
    this.target = target;
  }
}
