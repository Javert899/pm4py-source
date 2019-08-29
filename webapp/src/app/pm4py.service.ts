import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Pm4pyService {
  webservicePath: string;

  constructor(private http: HttpClient) {
    this.webservicePath = window.location.protocol+'//' + window.location.hostname + ':5000/';
  }

  getProcessSchema(parameters: HttpParams) {
    var completeUrl : string = this.webservicePath + "getProcessSchema";

    return this.http.get(completeUrl,{params: parameters});
  }
}
