import { Component, OnInit } from '@angular/core';
import { ScholarSearchService } from '../scholar-search.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  scholar = '';
  constructor(public scholarService: ScholarSearchService) { }

  ngOnInit(): void {
  }

  searchScholar(scholarName: string) {
    this.scholarService.searchScholar(scholarName);
  }

}
