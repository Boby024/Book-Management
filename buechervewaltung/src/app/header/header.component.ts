import { Component, OnInit } from '@angular/core';
import {AuthService} from '../auth.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(private auth: AuthService, private router: Router) { }

  ngOnInit() {
  }
  checkerLocalLogin() {
    return localStorage.getItem('email');
  }
 /*  checkerLocalSign() {
     if ( this.four-oh-four.signOut() === 'done' ) {
      return 'done';
    } else {
      return 'fail';
    }
  }*/
 deleteLocal() {
   localStorage.removeItem('email');
   window.location.reload();
 }
 signUP() {
   this.router.navigate(['/register']);
 }
 login() {
   this.router.navigate(['/login']);
 }
 home() {
   this.router.navigate(['/home']);
 }
 dashboard() {
   this.router.navigate(['/dashboard']);
 }
 getCurentUser() {
   return this.auth.currentUserValue;
 }

}
