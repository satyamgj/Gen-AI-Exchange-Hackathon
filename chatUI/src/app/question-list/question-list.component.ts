import { Component, Input } from '@angular/core';
import { Question } from '../question.model';

@Component({
    selector: 'app-question-list',
    templateUrl: './question-list.component.html',
    styleUrls: ['./question-list.component.css']
})
export class QuestionListComponent {
  @Input() results: any[] = []; // Replace 'any' with your result type if defined
}