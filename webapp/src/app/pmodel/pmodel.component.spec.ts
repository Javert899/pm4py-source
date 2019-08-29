import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PmodelComponent } from './pmodel.component';

describe('PmodelComponent', () => {
  let component: PmodelComponent;
  let fixture: ComponentFixture<PmodelComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PmodelComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PmodelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
