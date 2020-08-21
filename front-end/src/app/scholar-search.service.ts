import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';
import { map } from 'rxjs/operators';

import { environment } from '../environments/environment';
import { Scholar, ScholarJSON } from './scholar.model';

const BACKEND_URL = environment.apiUrl ;
@Injectable({
  providedIn: 'root'
})
export class ScholarSearchService {
  private scholars: Scholar[] = [];
  private scholarsUpdated = new Subject<{scholars: Scholar[]}>();

  constructor(private http: HttpClient) { }

  searchScholar(scholarName: string) {
    this.http.get(BACKEND_URL + 'scholar/' + scholarName)
      .pipe(map((scholarData: ScholarJSON) => {
        return {
          scholars: scholarData.scholars.map((scholar: Scholar) => {
            return {
              doctoral_advisor: scholar.doctoral_advisor,
              doctoral_student: scholar.doctoral_student,
              field: scholar.field,
              id: scholar.id,
              image_link: scholar.image_link,
              wiki_link: scholar.wiki_link,
              name: scholar.name
            };
          })
        };
      }))
      .subscribe((scholarData: ScholarJSON) => {
        this.scholars = scholarData.scholars;
        this.scholarsUpdated.next({scholars: this.scholars});
      });
  }

  getScholars() {
    this.http.get(BACKEND_URL)
      .pipe(map((scholarData: any) => {
        const scholarJson = JSON.parse(scholarData); // this still comes over as a string, so we have to parse it here
        return {
          scholars: scholarJson.scholars.map((scholar: Scholar) => {
            return {
              doctoral_advisor: scholar.doctoral_advisor,
              doctoral_student: scholar.doctoral_student,
              field: scholar.field,
              id: scholar.id,
              image_link: scholar.image_link,
              wiki_link: scholar.wiki_link,
              name: scholar.name
            };
          })
        };
      }))
      .subscribe((scholarData: ScholarJSON) => {
        this.scholars = scholarData.scholars;
        this.scholarsUpdated.next({scholars: this.scholars});
      });
  }

  getScholarUpdateListener() {
    return this.scholarsUpdated.asObservable();
  }
}
