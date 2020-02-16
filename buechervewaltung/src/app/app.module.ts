import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';
import {MatFormFieldModule, MatInputModule, MatSortModule, MatTableModule, MatPaginatorModule} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';




import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import {DataService } from './data.service';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HeaderComponent } from './header/header.component';
import {AuthService} from './auth.service';
import {AuthGuardService} from './auth-guard.service';
import {FourOhFourComponent} from './four-oh-four/four-oh-four.component';


const appRoutes: Routes = [
  { path: 'home', component: HomeComponent, canActivate: [AuthGuardService] },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuardService] },
  // { path: ' header', component: HeaderComponent, canActivate: [AuthGuardService] },
   // { path: 'not-found', component: FourOhFourComponent },
  // { path: '', redirectTo: 'not-found', pathMatch: 'full' },
   { path: '**', redirectTo: '/login' }
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    RegisterComponent,
    LoginComponent,
    DashboardComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatTableModule,
    RouterModule.forRoot(appRoutes, {enableTracing: true}),
    MatSortModule,
    MatFormFieldModule,
    MatInputModule,
    BrowserAnimationsModule,
    MatPaginatorModule,
    MatCardModule,
    MatButtonModule,
    // <-- debugging purposes only)
  ],
  providers: [HomeComponent, DataService, AuthService, LoginComponent, RegisterComponent, DashboardComponent ],
  bootstrap: [AppComponent]
})
export class AppModule { }
