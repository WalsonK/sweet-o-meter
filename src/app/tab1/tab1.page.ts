import { Component } from '@angular/core';
import { HistoriqueService } from '../shared/historique.service';
import { Prediction } from '../shared/models/prediction';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {

  historique: Prediction[] = []

  constructor(historiqueService: HistoriqueService) {
    this.historique = historiqueService.historique
  }

  goodPrediction(prediction: Prediction){
    prediction.isGood = 1;
  }

  badPrediction(prediction: Prediction){
    prediction.isGood = 2;
  }

}
