import { Component, OnInit } from '@angular/core';
import {Pm4pyService} from '../pm4py.service';
import { graphviz } from 'd3-graphviz';
import {HttpParams} from '@angular/common/http';


@Component({
  selector: 'app-pmodel',
  templateUrl: './pmodel.component.html',
  styleUrls: ['./pmodel.component.scss']
})
export class PmodelComponent implements OnInit {
  public gviz : string;
  public model : string;

  constructor(public pm4pyService : Pm4pyService) {
    this.gviz = "";
    this.model = "";

    this.getProcessSchema();
  }

  ngOnInit() {
  }

  getProcessSchema() {
    let httpParameters : HttpParams = new HttpParams();

    this.pm4pyService.getProcessSchema(httpParameters).subscribe(data => {
      let pm4pyJson = data as JSON;
      this.gviz = pm4pyJson['gviz'];
      this.model = pm4pyJson['model'];
      if (this.gviz == null || typeof(this.gviz) == "undefined") {
        this.gviz = "";
      }
      if (this.gviz.length > 0) {
        this.gviz = atob(this.gviz);
        this.model = atob(this.model);

        console.log(this.gviz);
        console.log(this.model);

        let targetInnerWidth = window.innerWidth * 0.75;
        let targetInnerHeight = window.innerHeight * 0.93;

        let targetWidth = window.innerWidth * 0.77;
        let targetHeight = window.innerHeight * 0.95;
      }

    });
  }

}
