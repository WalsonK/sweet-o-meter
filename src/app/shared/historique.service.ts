import { Injectable } from '@angular/core';
import { Prediction } from './models/prediction';

@Injectable({
  providedIn: 'root'
})
export class HistoriqueService {
  historique: Prediction[] = []

  constructor() {
    let pred0 = new Prediction();
    this.historique.push(pred0);
  }
}
