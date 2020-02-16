import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import { FormBuilder } from '@angular/forms';
import { Validators } from '@angular/forms';
import {stringify} from 'querystring';
import {DataService} from '../data.service';
import {User} from '../user';
import {Buch} from '../buch';
import {MatSort, MatPaginator, MatTableDataSource} from '@angular/material';
import {Resp} from '../resp';
import {AuthService} from '../auth.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
 buch = this.fb.group({
    titel: ['', Validators.required ],
    autor: ['', Validators.required ],
    verlag: ['', Validators.required ],
    erscheinungsjahr: ['', Validators.required ],
  });
 file: any ;
 response: any;
 users: any [];
 buecher: any [];
 foundBook: any [] = [];
 statusSearch = false;
 displayedColumns: string[] = ['id', 'titel', 'autor', 'verlag', 'erscheinungsjahr', 'status', 'ausgeliehen_am'];
 dataSource: MatTableDataSource<Buch[]>;
 public show = false;
 public buttonName: any = 'Show';
 resp: Resp;
 selectedBuch: Buch;
 feedback: any;

 @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
  @ViewChild(MatSort, {static: true}) sort: MatSort;

 constructor(private  fb: FormBuilder, private dataService: DataService, private auth: AuthService) {

 }

  ngOnInit() {
   // console.log( this.getUsers() );
   // console.log( this.getBuecher() );
    this.getBuecher();
    // this.getBooks();
  }
  applyFilter(filterValue: string) {
   console.log(filterValue);
   console.log(this.buecher);
   this.statusSearch = true;
   if (filterValue === ' ') {

    } else if (filterValue === '') {

    } else if (filterValue === undefined ) {
   } else {
     // this.dataSource = new MatTableDataSource(this.foundBook);
     this.foundBook = [];
      for (let i = 0; i < this.buecher.length; i++) {
        if ( this.buecher[i].titel.toLowerCase().indexOf( filterValue.toLowerCase() ) > -1) {
           this.foundBook.push(this.buecher[i]);
           console.log(this.foundBook);
        }
      }
      // this.foundBook = [];
      /* this.buecher = [];
      for ( let k = 0; k < this.foundBook.length; k++) {
        this.buecher[k] = this.foundBook[k];
      }
      this.foundBook = []; */
    }
  }
  getUsers() {
     console.log( this.dataService.getAllUsers().subscribe( data => { this.users =  data;  console.log(this.users); } )
     );
}
getBuecher() {
     // console.log( this.dataService.getAll_Buch().subscribe( data => { this.buecher =  data;  console.log(this.buecher); } )
  this.dataService.getAll_Buch().subscribe( data => {
    this.feedback = data;
    if ( !this.feedback.message) { this.buecher =  this.feedback; }
     } );
  }
  addBuch() {
    console.warn(JSON.stringify(this.buch.value));
    this.dataService.add_buch(JSON.stringify(this.buch.value)).subscribe(data => {
      this.response = data;
      // this.resp = data;
      window.location.reload();
    });
  }
  toggle() {
   this.show = !this.show;

    // CHANGE THE NAME OF THE BUTTON.
   if (this.show) {
      this.buttonName = 'Hide';
   } else {
      this.buttonName = 'Show';
    }
  }
  changeStatus( status: string) {
   if (status === 'in') {
     return 'verfügbar';
   } else {
     return status;
   }
  }
  getBooks() {
   this.dataSource = new MatTableDataSource(this.buecher);
   // this.dataSource.paginator = this.paginator;
   // this.dataSource.sort = this.sort;
  }
  // für Buch ausleihen
  buch_out(buch: Buch) {
   this.selectedBuch = buch;
   console.log(buch.id);
   const id = buch.id;
   const email = this.auth.currentUserValue;
   const dataToBackend: any = {id, email};
   this.dataService.buch_out(JSON.stringify(dataToBackend)).subscribe(data => {
      this.response = data;
      window.location.reload();
      console.warn(this.response);
    });
  }
   // für Buch zurückgeben
  buch_in(buch: Buch) {
   this.selectedBuch = buch;
   console.log(buch.id);
   const id = buch.id;
   const email = this.auth.currentUserValue;
   const dataToBackend: any = {id, email};
   this.dataService.buch_in(JSON.stringify(dataToBackend)).subscribe(data => {
      this.response = data;
      window.location.reload();
      console.warn(this.response);
    });
  }
  delete_buch(buch: Buch) {
   this.selectedBuch = buch;
   console.log(buch.id);
   const id = buch.id;
   const email = this.auth.currentUserValue;
   const dataToBackend: any = {id};
   this.dataService.delete_buch(JSON.stringify(dataToBackend)).subscribe(data => {
      this.response = data;
      window.location.reload();
      console.warn(this.response);
    });
  }
}
