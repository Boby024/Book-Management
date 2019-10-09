import { Injectable } from '@angular/core';
import {DataService} from './data.service';
import {User} from './user';

import {Router} from '@angular/router';
import {Resp} from './resp';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  user: User;
  resp: Resp;
  response: any;
  currentUserSubject: string;

  constructor(private dataService: DataService, private router: Router) {
  }
  public get currentUserValue() {
    this.currentUserSubject = localStorage.getItem('email');
    console.log(this.currentUserSubject);
    return this.currentUserSubject;
  }

  login(parameter: User) {
    console.warn(JSON.stringify(parameter));
    this.dataService.login(JSON.stringify(parameter)).subscribe(data => {
      this.response = data;
      this.resp = data;
      console.warn(this.resp);
      this.redirect(this.resp.message, this.resp.email);
    });
  }
  signUp(parameter: User) {
    console.warn(JSON.stringify( parameter));
    this.dataService.register(JSON.stringify(parameter)).subscribe( data => {
      this.response = data;
      this.resp = data;
      this.router.navigate(['/home']);
      localStorage.removeItem('email');
      localStorage.setItem('email', this.resp.email);
    });
  }

  redirect(parameter: string, parameterTwo: string) {
    if (parameter === 'login done') {
      this.router.navigate(['/home']);
      if (localStorage.getItem('email')) {
        localStorage.removeItem('email');
        localStorage.setItem('email', parameterTwo);
      } else { localStorage.setItem('email', parameterTwo); }
    } else {
      this.router.navigate(['/login']);
    }
  }

  signOut() {
    localStorage.getItem('email');
    localStorage.removeItem('email');
    return 'done';
  }



}
