import { TestBed } from '@angular/core/testing';

import { FastApiService } from './fast-api.service';

describe('FastApiService', () => {
  let service: FastApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FastApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
