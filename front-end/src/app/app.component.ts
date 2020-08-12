import { Component } from '@angular/core';
import APP_CONFIG from './app.config';
import { Node, Link } from './d3/models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Web of Scholars';

  nodes: Node[] = [];
  links: Link[] = [];

  scholars = APP_CONFIG.SCHOLARS; // start with some base scholars, need to implement on changes with
  //this variable that way can reset this variable and update the whole web

  constructor() {
    this.setUpNodes();
    this.setUpLinks();
  }

  /**
   * constructing the nodes array
  */
  setUpNodes() {
    for (let i = 0; i < this.scholars.length; i++) {
      const scholar = this.scholars[i];
      this.nodes.push(new Node(scholar.id, scholar.name));
    }
  }

  /**
   *  constructs links between related scholars
   */
  setUpLinks() {
    for (let i = 0; i < this.scholars.length; i++) {
      const cur_scholar = this.scholars[i];
      const doctoral_advisors = cur_scholar['doctoral_advisor'];
      doctoral_advisors.push(...cur_scholar['academic_advisor']);
      if (doctoral_advisors) {
        for (let j = 0; j < doctoral_advisors.length; j++) {
          this.findAdvisor(i, doctoral_advisors[j]);
        }
      }
    }
  }

  /**
   * finds a given scholar's advisor
   * @param {scholar} scholar index in the scholars array
   * @param {string} advisor_qid
   */
  findAdvisor(scholar_index, advisor_qid) {
    for (let i = 0; i < this.scholars.length; i++) {
      if (this.scholars[i].id === advisor_qid) {
        this.links.push(new Link(this.nodes[i], this.nodes[scholar_index]));
      }
    }
  }
}
