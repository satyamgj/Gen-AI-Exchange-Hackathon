import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class QueryService {

  constructor(private http: HttpClient) { }


  getResults(query: string): Observable<any> {
    let _json = {
      "query":query
    }
    return this.http.post("http://127.0.0.1:8000/api/v1/query",_json)
  }

  getOtherQuestions(query: string): Observable<any> {
    let _json = {
      "query":query
    }
    return this.http.post("http://127.0.0.1:8000/api/v1/relatedQuestions",_json)
  }

  getChatReply(query: string,past_replies:string[]): Observable<any> {
    let _json = {
      "query":query,
      "past_replies":past_replies
    }
    return this.http.post("http://127.0.0.1:8000/api/v1/chat",_json)
  }
}