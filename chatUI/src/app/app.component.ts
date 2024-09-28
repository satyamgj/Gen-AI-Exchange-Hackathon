import { Component } from '@angular/core';
import { QueryService } from './query-service.service'; // Import your API service

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  results: any[] = [];
  otherQuestions:any[]=[];
  loading = false;
  error = false;
  pastQuestions: string[] = []; // Array to hold past questions
  pastReplies:string[]=[];

  constructor(private apiService: QueryService) {}

  onQuerySubmitted(query: string) {
    this.loading = true;
    this.error = false;


    // Add the new question to the past questions array
    this.pastQuestions.unshift(query); // Add new question at the start
    if (this.pastQuestions.length > 5) {
      this.pastQuestions.pop(); // Keep only the last five questions
    }
    if(this.results.length > 0 ){
      this.results.forEach((_json)=>{
        this.pastReplies.unshift(_json['answer'])
        console.log(this.pastReplies.length > 0)
      })
      this.apiService.getChatReply(query,this.pastReplies).subscribe((result)=>{
        this.results.unshift(result);
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching results:', error);
        this.error = true;
        this.loading = false;
      })
    }else{

      this.apiService.getResults(query).subscribe(
        (result) => {
          this.results.unshift(result);
          this.loading = false;
        },
        (error) => {
          console.error('Error fetching results:', error);
          this.error = true;
          this.loading = false;
        }
      );
    }
   

    this.apiService.getOtherQuestions(query).subscribe(
      (result) => {
        this.otherQuestions = []
        // Split the paragraph by line breaks or numbers followed by periods
        const splitRegex = /\d\.\s+/;
        const lines = result.split(splitRegex);

  // The first split will be an empty string, so we remove it
lines.shift();

// Push all the lines into an array

lines.forEach((line: string) => {
  this.otherQuestions.unshift(line.trim());
});
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching results:', error);
        this.error = true;
        this.loading = false;
      }
    );
  }
}