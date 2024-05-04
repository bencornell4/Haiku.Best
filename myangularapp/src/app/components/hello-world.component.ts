import { Component, Injectable, importProvidersFrom } from "@angular/core";
import { FormsModule } from '@angular/forms';
import { HttpClient } from "@angular/common/http";
import { CommonModule } from '@angular/common';

@Component({
    standalone: true,
    selector: 'app-hello-world',
    templateUrl: './hello-world.component.html',
    imports: [FormsModule, CommonModule],
})

@Injectable({
    providedIn: 'root'
})
export class HelloWorldComponent {
    message: string = 'enter a haiku:';
    content: string = '';
    author: string = '';
    score: number = 0;

    constructor(private http: HttpClient) {}

    submitHaiku(): void {
        this.http.post('http://127.0.0.1:8080/api/haikujudge/', { 
            content: this.content,
            author: this.author,
            score: this.score
        }).subscribe((response: any) => {
            this.score = response.score;
        });
    }
}