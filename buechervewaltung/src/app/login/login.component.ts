import { Component, OnInit } from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {DataService} from '../data.service';
import {Router} from '@angular/router';
// @ts-ignore
import {Resp} from '../resp';
import {AuthService} from '../auth.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
user = this.fb.group({
    email: ['', Validators.required ],
    passwort: ['', Validators.required ],
  });
 file: any ;
 response: any;
 resp: Resp;
 users: any []

 constructor(private  fb: FormBuilder, private dataService: DataService, private router: Router, private auth: AuthService) { }

  ngOnInit() {
  }

onSubmit() {
  // TODO: Use EventEmitter with form value
 this.auth.login( this.user.value );
}


}
