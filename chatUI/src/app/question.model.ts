// src/app/question.model.ts
export interface Question {
    id: number;
    text: string;
    answer?: string; // Optional, as it may not be answered yet
}