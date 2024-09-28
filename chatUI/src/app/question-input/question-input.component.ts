import { Component, EventEmitter, Output } from '@angular/core';
import { Question } from '../question.model';

@Component({
    selector: 'app-question-input',
    templateUrl: './question-input.component.html',
    styleUrls: ['./question-input.component.css']
})
export class QuestionInputComponent {
  queryText: string = '';

  @Output() querySubmitted = new EventEmitter<string>();

  submitQuery() {
    if (this.queryText.trim()) {
      this.querySubmitted.emit(this.queryText);
      this.queryText = ''; // Clear input field after submission
    }
  }
}