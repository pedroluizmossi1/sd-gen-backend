import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError, of } from 'rxjs';
import { catchError, retry, tap } from 'rxjs/operators';
import { CookieService } from 'ngx-cookie-service';
import { HttpResponse } from '@capacitor/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class FastApiService {
  static checkToken() {
    throw new Error('Method not implemented.');
  }

  constructor(private http: HttpClient, private cookieService: CookieService, private router: Router) {    
    this.url = 'http://192.168.100.44:8000';
    
  }
  private url: string;

  static loginUser(username: string, password: string) {
    throw new Error('Method not implemented.');
  }

  loginUser(username: string, password: string): Observable<any> {
    const body = { "login": username, "password": password };
    const response = this.http.post( this.url +'/auth/login', body);
    
    return response.pipe(
      catchError((error) => {
        alert(JSON.stringify(error.error));
        return throwError(error);
      }),
      tap((res: any) => {
        this.cookieService.set('token', res.token);
        this.cookieService.set('isAuthenticated', 'true');
        this.cookieService.set('user', username.toLowerCase());
        this.router.navigate(['/tabs']);
      })
    );
  }

  logoutUser(): Observable<any> {
    const body = { "token": this.cookieService.get('token'), "user": this.cookieService.get('user') };
    const response = this.http.post( this.url +'/auth/logout', body);
    return response.pipe(
      catchError((error) => {
        return throwError(error);
      }),
      tap((res: any) => {
        this.cookieService.delete('token');
        this.cookieService.delete('isAuthenticated');
        this.cookieService.delete('user');
        this.router.navigate(['/login']);
      })
    );
  }

  registerUser(username: string, password: string, email: string, firstName: string, lastName: string): Observable<any> {
    const body = { "login": username, "password": password, "email": email, "first_name": firstName, "last_name": lastName };
    const response = this.http.post( this.url +'/user/register', body);
    return response.pipe(
      catchError((error) => {
        alert(JSON.stringify(error.error));
        return throwError(error);
      }),
      tap((res: any) => {
        this.router.navigate(['/login']);
      })
    );
  }

  getUserProfile(): Observable<any> {
    const user = this.cookieService.get('user');
    const headers = { 'Authorization': 'Bearer ' + this.cookieService.get('token') };
    const response = this.http.get(this.url + '/user/profile/' + user, { headers});
    return response.pipe(
      catchError((error) => {
        return throwError(error);
      }),
      tap((res: any) => {
        return res;
      })
    );
  }

  updateUserProfile(email: string, firstName: string, lastName: string): Observable<any> {
    const user = this.cookieService.get('user');
    const body = { "email": email, "first_name": firstName, "last_name": lastName };
    const headers = { 'Authorization': 'Bearer ' + this.cookieService.get('token') };
    const response = this.http.post(this.url + '/user/profile/' + user, body, { headers});
    return response.pipe(
      catchError((error) => {
        return throwError(error);
      }),
      tap((res: any) => {
        return res;
      })
    );
  }

  //check token if true return true else return false
  checkToken(token:string): Observable<boolean> {
    const response = this.http.get( this.url +'/auth/check/', {params: new HttpParams().set('token', token)});
    //the api return true when token is valid
    return response.pipe(
      catchError((error) => {
        return of(false);
      }
      ),
      retry(3),
      tap((res: any) => {
        if (res === true) {
          return of(true);
        } else {
          return of(false);
        }
      }
      )
    );
  }

}

