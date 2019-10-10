import { Component, OnInit } from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {DataService} from '../data.service';
import {Router} from '@angular/router';
import {AuthService} from '../auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
 user = this.fb.group({
    email: ['', Validators.email ],
    passwort: ['', Validators.minLength(5) ],
  });
 file: any ;
 response: any;
 users: any []

 constructor(private  fb: FormBuilder, private dataService: DataService, private router: Router, private auth: AuthService) { }

  ngOnInit() {
  }
  onSubmit() {
  // TODO: Use EventEmitter with form value
  console.warn(JSON.stringify( this.user.value));
  this.auth.signUp(this.user.value);

  }

}
