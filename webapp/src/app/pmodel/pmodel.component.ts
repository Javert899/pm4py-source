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
  public model_type_variant : string;
  public rel_ev_variant : string;
  public node_freq_variant : string;
  public edge_freq_variant : string;

  constructor(public pm4pyService : Pm4pyService) {
    this.gviz = "";
    this.model = "";
    this.model_type_variant = "model1";
    this.rel_ev_variant = "rel_dfg";
    this.node_freq_variant = "type1";
    this.edge_freq_variant = "type11";

    this.getProcessSchema();
  }

  ngOnInit() {
  }

  getProcessSchema() {
    let httpParameters : HttpParams = new HttpParams();
    httpParameters = httpParameters.set("model_type_variant", this.model_type_variant);
    httpParameters = httpParameters.set("rel_ev_variant", this.rel_ev_variant);
    httpParameters = httpParameters.set("node_freq_variant", this.node_freq_variant);
    httpParameters = httpParameters.set("edge_freq_variant", this.edge_freq_variant);


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

        let currentWidth = parseInt(this.model.split("width=\"")[1].split("pt\"")[0]);
        let currentHeight = parseInt(this.model.split("height=\"")[1].split("pt\"")[0]);

        let ratioWidth : number = targetInnerWidth / currentWidth;
        let ratioHeight : number = targetInnerHeight / currentHeight;

        let ratio : number = Math.min(ratioWidth, ratioHeight);

        let thisEl = graphviz('#dotProvidedDiv').width(targetWidth+'px').height(targetHeight+'px').renderDot(this.gviz);

        let dotProvidedDiv = document.getElementById("dotProvidedDiv");
        let svgDoc = dotProvidedDiv.childNodes;

        (<SVGSVGElement>svgDoc[0]).currentScale = ratio;
      }

    });
  }

  typeOfModelChanged() {
    this.model_type_variant = (<HTMLInputElement>document.getElementById("pmodelSelect")).value;

    if (this.model_type_variant == "model1") {
      this.node_freq_variant = "type1";
      this.edge_freq_variant = "type11";
    }
    else if (this.model_type_variant == "model2") {
      this.node_freq_variant = "type21";
      this.edge_freq_variant = "type211";
    }
    else if (this.model_type_variant == "model3") {
      this.node_freq_variant = "type31";
      this.edge_freq_variant = "type11";
    }
    (<HTMLInputElement>document.getElementById("nodeFreqSelect")).value = this.node_freq_variant;
    (<HTMLInputElement>document.getElementById("edgesFreqSelect")).value = this.edge_freq_variant;

    this.getProcessSchema();
  }

  typeOfEventSelectionChanged() {
    this.rel_ev_variant = (<HTMLInputElement>document.getElementById("relEventSelect")).value;
    this.getProcessSchema();
  }

  typeOfNodeFreqChanged() {
    this.node_freq_variant = (<HTMLInputElement>document.getElementById("nodeFreqSelect")).value;
    if (this.node_freq_variant == "type1") {
      this.edge_freq_variant = "type11";
    }
    else if (this.node_freq_variant == "type21") {
      this.edge_freq_variant = "type211";
    }
    else if (this.node_freq_variant == "type22") {
      this.edge_freq_variant = "type221";
    }
    else if (this.node_freq_variant == "type23") {
      this.edge_freq_variant = "type231";
    }
    else if (this.node_freq_variant == "type31") {
      this.edge_freq_variant = "type11";
    }
    else if (this.node_freq_variant == "type32") {
      this.edge_freq_variant = "type12";
    }
    else if (this.node_freq_variant == "type32") {
      this.edge_freq_variant = "type13";
    }
    (<HTMLInputElement>document.getElementById("edgesFreqSelect")).value = this.edge_freq_variant;

    this.getProcessSchema();
  }

  typeOfEdgesFreqChanged() {
    this.edge_freq_variant = (<HTMLInputElement>document.getElementById("edgesFreqSelect")).value;
    this.getProcessSchema();
  }
}
