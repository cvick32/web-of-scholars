import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription, Subject } from 'rxjs';

import { Node, Link } from './d3/models';
import { ScholarSearchService } from './scholar-search.service';
import { Scholar } from './scholar.model';
import { NodesAndLinks } from './nodes-and-links.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Web of Scholars';

  scholars: Scholar[];
  nodes: Node[] = [];
  links: Link[] = [];

  currentNodesAndLinks =  new Subject<NodesAndLinks>();

  private scholarsSub: Subscription;

  constructor(public scholarService: ScholarSearchService) { }

  ngOnInit() {
    this.scholarService.getScholars();

    this.scholarsSub = this.scholarService.getScholarUpdateListener()
      .subscribe((scholarData: {scholars: Scholar[]}) => {
        console.log(scholarData.scholars);
        this.scholars = scholarData.scholars;
        this.setUpNodes();
        this.setUpLinks();
        this.currentNodesAndLinks.next({nodes: this.nodes, links: this.links});
      });
  }

  ngOnDestroy() {
    this.scholarsSub.unsubscribe();
  }

  /**
   * constructing the nodes array
  */
  setUpNodes(): void {
    this.nodes = [];
    for (const scholar of this.scholars) {
      this.nodes.push(new Node(scholar.id, scholar.name, scholar.wiki_link));
    }
  }

  /**
   *  constructs links between related scholars
   */
  setUpLinks(): void {
    this.links = [];
    for (const scholar of this.scholars) {
      const doctoral_advisors = scholar.doctoral_advisor;
      if (doctoral_advisors) {
        for (const advisor of doctoral_advisors) {
          this.findAdvisor(scholar, advisor);
        }
      }
    }
  }

  /**
   * finds a given scholar's advisor
   * @param {scholar} scholar index in the scholars array
   * @param {string} advisor_qid
   */
  findAdvisor(scholar: Scholar, advisor_qid: string): void {
    for (const advisor of this.scholars) {
      if (advisor.id === advisor_qid) {
        this.links.push(new Link(this.scholarToNode(advisor), this.scholarToNode(scholar)));
      }
    }
  }

  /**
   * Returns the Node associated with the given scholar
   * @param scholar scholar whose node we are looking for
   */
  scholarToNode(scholar: Scholar): Node {
    for (const node of this.nodes) {
      if (node.id === scholar.id) {
        return node;
      }
    }
  }
}
