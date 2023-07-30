import { Component } from '@angular/core';
import { ToastController } from '@ionic/angular';
import { ParametreService } from '../shared/parametre.service';

@Component({
  selector: 'app-tab3',
  templateUrl: 'tab3.page.html',
  styleUrls: ['tab3.page.scss']
})
export class Tab3Page {

  color: string = "l";
  ia : string = "rust"
  size: string = "15";

  constructor(private toastCtrl: ToastController, private parametreService: ParametreService) {}

  isDisabled(pixel: number): boolean {
    if (this.color === 'rgb' && (pixel == 50 || pixel == 25)) {
      return true;
    } else if (this.color === 'l' && pixel == 50) {
      return true;
    }
    return false;
  }

  resetSize(){
    if(this.color == "rgb" && (this.size == "50" || this.size == "25")){
      this.size = ""
    }
    if(this.color == "l" && this.size == "50"){
      this.size = ""
    }
  }

  async presentToast() {
    const toast = await this.toastCtrl.create({
      message: 'Les paramètres ont été sauvegardé !',
      duration: 1500,
      position: 'bottom',
      color: 'success'
    });

    await toast.present();
  }

  save(){
    this.parametreService.ia = this.ia;
    this.parametreService.color = this.color;
    this.parametreService.size = this.size;
    this.presentToast()
  }
}
