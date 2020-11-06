import { Component, Input, OnInit, AfterViewInit, HostListener, ChangeDetectorRef } from '@angular/core';
import { Subject } from 'rxjs';

import { ForceDirectedGraph } from '../d3/models/index';
import { D3Service } from '../d3/d3.service';
import { NodesAndLinks } from '../nodes-and-links.model';
import { Node, Link } from '../d3/models/index';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit, AfterViewInit {
  @Input('currentNodesAndLinks') currentNodesAndLinks: Subject<NodesAndLinks>;

  graph: ForceDirectedGraph;

  links$ = new Subject<Link[]>();
  nodes$ = new Subject<Node[]>();

  private _options: {width, height} = {width: 800, height: 600};

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.graph.initSimulation(this.options);
  }

  constructor(private d3Service: D3Service, private ref: ChangeDetectorRef) {}

  ngOnInit() {
    this.currentNodesAndLinks.subscribe(nodesAndLinks => {
      this.nodes$.next(nodesAndLinks.nodes);
      this.links$.next(nodesAndLinks.links);
      this.graph = this.d3Service.getForceDirectedGraph(nodesAndLinks.nodes, nodesAndLinks.links, this.options);
      this.graph.ticker.subscribe((d) => {
        this.ref.markForCheck();
      });
      this.graph.initSimulation(this.options);
    });
  }

  ngAfterViewInit(): void {
    this.graph.initSimulation(this.options);
  }

  navigateToWikiLink(link: string) {
    window.open(link, '_blank');
  }

  get options() {
    return this._options = {
      width: window.innerWidth,
      height: window.innerHeight
    };
  }

}
