import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {User} from './user';
import {Router} from '@angular/router';
import {Buch} from './buch';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private url = 'http://localhost:5001/';
  private socket;
  user: User;
  users: User[];
  buch: Buch;
  buecher: Buch[];
  fehler = 'wow Fehler';
  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      // 'Authorization': 'my-four-oh-four-token'
    })
  };
  constructor(private http: HttpClient, private router: Router ) {
  }

  register(data: string): Observable<User> {
    console.log(data);
    // console.log( JSON.stringify( data ) )
    return this.http.post<User>('/api/register', data, this.httpOptions);
  }
   getAllUsers(): Observable<User[] > {
    return this.http.get<User[]>('/api/users');
  }
  login(data: string): Observable<User> {
    console.log(data);
    // console.log( JSON.stringify( data ) )
    return this.http.post<User>('/api/login', data, this.httpOptions);
  }


  getAll_Buch(): Observable<Buch[] > {
    // console.log( JSON.stringify( data ) )
    return this.http.get<Buch[]>('/api/all_Buch');
  }
  // Wir erwarten hier : titel, autor, verlag und ercheinungsjahr
   add_buch(data: string): Observable<Buch> {
    console.log(data);
    // console.log( JSON.stringify( data ) )
    return this.http.post<Buch>('/api/add_buch', data, this.httpOptions);
  }
  // Nur id des Buchs wird  beim Löschen erwartet
   delete_buch(data: any): Observable<any> {
    console.log(data);
    // console.log( JSON.stringify( data ) )
    return this.http.post<any>('/api/delete_buch', data, this.httpOptions);
  }
  // id -buch und email des Users werden erwartet
  buch_out(data: any): Observable<any> {
    console.log(data);
    // console.log( JSON.stringify( data ) )
    return this.http.put<any>('/api/buch_out', data, this.httpOptions);
  }
  // Nur id -buch wird  erwartet
  buch_in(data: any): Observable<any> {
    console.log(data);
    // console.log( JSON.stringify( data ) )
    return this.http.put<any>('/api/buch_in', data, this.httpOptions);
  }
}
