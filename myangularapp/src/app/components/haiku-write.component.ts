import { Component, ViewChild, ElementRef, Injectable, isDevMode, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { FormsModule } from '@angular/forms';
import { HttpClient } from "@angular/common/http";
import { NgIconComponent, provideIcons } from '@ng-icons/core'
import { heroQuestionMarkCircle, heroTrophy, heroXCircle, heroShare} from '@ng-icons/heroicons/outline'
import { NgxSpinnerService } from "ngx-spinner";
import { CommonModule } from "@angular/common";
import { NgxSpinnerModule } from 'ngx-spinner';

var serverUrl = 'https://server.haiku.best/'
if (isDevMode()) {
    serverUrl = 'http://localhost:8000/'
}

@Component({
    standalone: true,
    selector: 'app-haiku-write',
    templateUrl: './haiku-write.component.html',
    imports: [
            FormsModule, NgIconComponent, CommonModule, NgxSpinnerModule
        ],
    viewProviders: [provideIcons({ heroQuestionMarkCircle, heroTrophy, heroXCircle, heroShare})],
    schemas: [CUSTOM_ELEMENTS_SCHEMA],
})

@Injectable({
    providedIn: 'root'
})
export class HaikuWriteComponent {
    @ViewChild('scoreDialog') scoreDialog!: ElementRef;
    @ViewChild('leaderDialog') leaderDialog!: ElementRef;
    @ViewChild('limitDialog') limitDialog!: ElementRef;
    line1: string = '';
    line2: string = '';
    line3: string = '';
    author: string = '';
    score: number = 0;
    haiku1: [string, string, number] = ['', '', 0]

    constructor(private http: HttpClient, private spinner: NgxSpinnerService) {
        this.spinner.show()
        this.http.head(serverUrl + "api/")
            .subscribe((response: any) => {
                this.spinner.hide()
            });
    }

    getTopHaiku(): void {
        this.spinner.show()
        this.http.get(serverUrl + "api/haikutop/")
            .subscribe((response: any) => {
                this.leaderDialog.nativeElement.open = true;
                this.haiku1[0] = response[0]['content']
                this.haiku1[1] = response[0]['author']
                this.haiku1[2] = response[0]['score']
                console.log(this.haiku1[0])
                this.spinner.hide();
            });
    }

    submitHaiku(): void {
        this.spinner.show()
        this.http.post(serverUrl + "api/haikujudge/", {
            content: this.line1 + "\n " + this.line2 + "\n " + this.line3,
            author: this.author,
            score: this.score,
        }, {withCredentials: true}).subscribe((response: any) => {
            if (response.message) {
                this.limitDialog.nativeElement.open = true;
                this.spinner.hide();
            } else {
                this.score = response.score;
                this.scoreDialog.nativeElement.open = true;
                this.spinner.hide();
            }
        });
    }
}
