import { Component, OnDestroy, OnInit } from '@angular/core';
import { CameraPreview, CameraPreviewOptions, CameraPreviewPictureOptions, CameraSampleOptions } from '@capacitor-community/camera-preview';

import '@capacitor-community/camera-preview'
import { EventsService } from '../shared/events.service'
import { Camera, ImageOptions, CameraResultType, CameraSource } from '@capacitor/camera';
import { ApiService } from '../shared/api.service';
import { ParametreService } from '../shared/parametre.service';
import { Prediction } from '../shared/models/prediction';
import { HistoriqueService } from '../shared/historique.service';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page implements OnInit, OnDestroy{
  tab2btnClickSub : any;
  image = null;
  cameraActive = false;
  isModalOpen = false;

  prediction: Prediction = new Prediction();

  constructor(
    private eventsService: EventsService,
    private apiService: ApiService,
    private parametreService: ParametreService,
    private historiqueService: HistoriqueService) {}

  ngOnInit(): void {
    this.openCamera();
    this.tab2btnClickSub = this.eventsService.onTab2ButtonClick().subscribe(() => {
      if(this.cameraActive){
        this.captureImage();
      }
    })
  }

  openCamera(){
    const cameraPreviewOptions: CameraPreviewOptions = {
      position: 'front',
      parent: 'cameraPreview',
      className: 'cameraPreview'
    };
    CameraPreview.start(cameraPreviewOptions);
    this.cameraActive = true;
  }

  async stopCamera(){
    await CameraPreview.stop();
    this.cameraActive = false;
  }

  async captureImage(){
    const CameraPreviewPictureOptions: CameraPreviewPictureOptions = {
      quality: 85
    };

    const result = await CameraPreview.capture(CameraPreviewPictureOptions);
    const data = {
      base64 : result.value,
      ia : this.parametreService.ia,
      color : this.parametreService.color,
      size : this.parametreService.size
    }
    this.apiService.sendImage(data).subscribe(result => {
      this.prediction = result;
      this.setOpenModal();
    })
    this.stopCamera();
  }

  flipCamera(){
    CameraPreview.flip();
  }

  async uploadPicture(){
    const imageOptions : ImageOptions = {
      resultType: CameraResultType.Base64,
      source: CameraSource.Photos
    }
    try {
      const img = await Camera.getPhoto(imageOptions);
      const base64Image = img.base64String;
      if(this.cameraActive) this.stopCamera();

      const data = {
        base64 : base64Image,
        ia : this.parametreService.ia,
        color : this.parametreService.color,
        size : this.parametreService.size
      }

      this.apiService.sendImage(data).subscribe(result => {
        this.prediction = result;
        this.setOpenModal();
      })
    }
    catch(e){
      console.log('Erreur :', e);
    }
  }

  ngOnDestroy(): void {
    this.tab2btnClickSub.unsubsribe();
  }

  setOpenModal(){
    if(this.isModalOpen == false){
      this.isModalOpen = true;
    }else{
      this.isModalOpen = false;
    }
  }

  goodPredict(pred: Prediction){
    pred.isGood = 1;
    pred.id = this.historiqueService.historique.length
    this.setOpenModal();
    this.historiqueService.historique.push(pred)
  }

  badPredict(pred : Prediction){
    pred.isGood = 2;
    pred.id = this.historiqueService.historique.length
    this.setOpenModal();
    this.historiqueService.historique.push(pred)
  }
}
