import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private url = environment.backendServer

  constructor(private http: HttpClient) { }

  sendImage(base64: string): Observable<any>{
    return this.http.post<any>(this.url + "predict", {data: base64});
  }
}
