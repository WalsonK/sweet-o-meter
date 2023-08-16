import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { EventsService } from './shared/events.service';
import { ApiService } from './shared/api.service';
import { HttpClientModule } from '@angular/common/http';
import { ParametreService } from './shared/parametre.service';
import { HistoriqueService } from './shared/historique.service';

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule, HttpClientModule],
  providers: [{ provide: RouteReuseStrategy, useClass: IonicRouteStrategy }, EventsService, ApiService, ParametreService, HistoriqueService],
  bootstrap: [AppComponent],
})
export class AppModule {}
