import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EventsService {
  private tab2ButtonClickSubject = new Subject<void>();

  triggerTab2ButtonClick() {
    this.tab2ButtonClickSubject.next();
  }

  onTab2ButtonClick() {
    return this.tab2ButtonClickSubject.asObservable();
  }
}
