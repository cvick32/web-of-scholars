import { Directive, Input, ElementRef, OnInit } from '@angular/core';
import { D3Service } from '../d3.service';

@Directive({
  // tslint:disable-next-line: directive-selector
  selector: '[zoomable]'
})
export class ZoomableDirective implements OnInit {
  // tslint:disable-next-line: no-input-rename
  @Input('zoomable') zoomableOf: ElementRef;

  constructor(private d3Service: D3Service, private _element: ElementRef) {}

  ngOnInit() {
    this.d3Service.applyZoomableBehavior(this.zoomableOf, this._element.nativeElement);
  }
}
