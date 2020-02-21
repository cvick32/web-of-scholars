import { BrowserModule } from '@angular/platform-browser';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { AppComponent } from './app.component';
import { DraggableDirective } from './d3/directives/draggable.directive';
import { ZoomableDirective } from './d3/directives/zoomable.directive';
import { D3Service } from './d3/d3.service';

import { GraphComponent } from './graph/graph.component';

@NgModule({
  declarations: [
    AppComponent,
    DraggableDirective,
    ZoomableDirective,
    GraphComponent
  ],
  imports: [
    BrowserModule
  ],
  schemas: [NO_ERRORS_SCHEMA],
  providers: [D3Service],
  bootstrap: [AppComponent]
})
export class AppModule { }
