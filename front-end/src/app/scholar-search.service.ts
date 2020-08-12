import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ScholarSearchService {

  constructor(private http: HttpClient) { }

  search(scholar: string) {
    /**
     * Call python api
     */
  }
}
