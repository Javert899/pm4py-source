import { TestBed } from '@angular/core/testing';

import { Pm4pyService } from './pm4py.service';

describe('Pm4pyService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: Pm4pyService = TestBed.get(Pm4pyService);
    expect(service).toBeTruthy();
  });
});
