import { Component, OnDestroy, OnInit } from '@angular/core';
import { CameraPreview, CameraPreviewOptions, CameraPreviewPictureOptions, CameraSampleOptions } from '@capacitor-community/camera-preview';

import '@capacitor-community/camera-preview'
import { EventsService } from '../shared/events.service'
import { Camera, ImageOptions, CameraResultType, CameraSource } from '@capacitor/camera';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page implements OnInit, OnDestroy{
  tab2btnClickSub : any;
  image = null;
  cameraActive = false;

  constructor(private eventsService: EventsService) {}

  ngOnInit(): void {
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
    const base64Picture = result.value;
    console.log(base64Picture)
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
      console.log(base64Image)
    }
    catch(e){
      console.log('Erreur :', e);
    }
  }

  ngOnDestroy(): void {
    this.tab2btnClickSub.unsubsribe();
  }
}
