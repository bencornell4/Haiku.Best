import { Component, ViewChild, ElementRef, Injectable, isDevMode } from "@angular/core";
import { FormsModule } from '@angular/forms';
import { HttpClient } from "@angular/common/http";
import { CommonModule } from '@angular/common';
import { NgIconComponent, provideIcons } from '@ng-icons/core'
import { heroBars3, heroQuestionMarkCircle, heroTrophy, heroCog6Tooth, heroXCircle, heroShare} from '@ng-icons/heroicons/outline'

@Component({
    standalone: true,
    selector: 'app-hello-world',
    templateUrl: './hello-world.component.html',
    imports: [FormsModule, CommonModule, NgIconComponent],
    viewProviders: [provideIcons({ heroBars3, heroQuestionMarkCircle, heroTrophy, heroCog6Tooth, heroXCircle, heroShare})],
})

@Injectable({
    providedIn: 'root'
})
export class HelloWorldComponent {
    @ViewChild('scoreDialog') scoreDialog!: ElementRef;
    line1: string = '';
    line2: string = '';
    line3: string = '';
    author: string = '';
    score: number = 0;

    constructor(private http: HttpClient) {}

    submitHaiku(): void {
        var serverUrl = 'https://haiku-best.onrender.com/api/haikujudge/'
        if (isDevMode()) {
            serverUrl = 'http://localhost:8000/api/haikujudge/'
        }
        this.http.post(serverUrl, {
            content: this.line1 + ", " + this.line2 + ", " + this.line3,
            author: this.author,
            score: this.score
        }).subscribe((response: any) => {
            this.score = response.score;
            this.scoreDialog.nativeElement.open = true;
            console.log(response.score)
        });
    }
}
