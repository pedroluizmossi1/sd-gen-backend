import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { FastApiService } from './fast-api.service';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private FastApiService: FastApiService, private router: Router, private cookieService: CookieService) {}

  canActivate(): boolean {
    const tokenValidate = this.FastApiService.checkToken(this.cookieService.get('token')).subscribe(
      //if response is true
      (response) => {
        if (response === true) {
          return true;
        } else {
          this.router.navigate(['/login']);
          return false;
        }
      }
    );
    return true;
  }
}