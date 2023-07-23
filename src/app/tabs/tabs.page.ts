import { Component, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { IonTabButton, IonTabs } from '@ionic/angular';
import { EventsService } from '../shared/events.service';

@Component({
  selector: 'app-tabs',
  templateUrl: 'tabs.page.html',
  styleUrls: ['tabs.page.scss']
})
export class TabsPage {
  @ViewChild('tabs') tabs!: IonTabs;

  constructor(private eventsService: EventsService) {}

  captureImage(){
    if(this.tabs.getSelected() === "tab2"){
      this.eventsService.triggerTab2ButtonClick();
    }
  }
}
