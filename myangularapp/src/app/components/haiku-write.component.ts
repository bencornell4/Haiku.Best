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

var isLoaded = false

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
    @ViewChild('infoDialog') infoDialog!: ElementRef;
    @ViewChild('warningDialog') warningDialog!: ElementRef;
    line1: string = '';
    line2: string = '';
    line3: string = '';
    author: string = '';
    score: number = 0;
    percentile: number = 0;
    haikus: [string, string, number][] = [];

    constructor(private http: HttpClient, private spinner: NgxSpinnerService) {}

    ngOnInit() {
        //init leaderboard
        for (let i = 0; i < 3; i++) {
            this.haikus.push(['', '', 0]);
        }
        //init spinner
        this.spinner.show("spinnerStart");
        //check connection
        this.http.get(serverUrl + "api/", {
            withCredentials: true
        }).subscribe((response: any) => {
            this.spinner.hide("spinnerStart");
            isLoaded = true;
            if(response['alreadySubmitted']) {
                this.score = response['lastScore'];
                this.percentile = response['lastPercentile'];
                this.limitDialog.nativeElement.open = true;
                this.infoDialog.nativeElement.open = false;
            }
        });
     }

    getTopHaiku(): void {
        if (isLoaded) {
            this.spinner.show("spinnerMain");
            this.http.get(serverUrl + "api/haikutop/")
            .subscribe((response: any) => {
                this.haikus.forEach((element: any, index) => {
                    console.log(element);
                    element[0] = response[index]['content'];
                    element[1] = response[index]['author'];
                    element[2] = response[index]['score'];
                    this.spinner.hide("spinnerMain");
                });
                console.log(this.haikus);
                this.leaderDialog.nativeElement.open = true;
            });
        } else {
            this.warningDialog.nativeElement.open = true;
        }
    }

    submitHaiku(): void {
        if (isLoaded) {
            this.spinner.show("spinnerMain")
            this.http.post(serverUrl + "api/haikujudge/", {
                content: this.line1 + "\n " + this.line2 + "\n " + this.line3,
                author: this.author,
                score: this.score,
            }, {withCredentials: true}).subscribe((response: any) => {
                if (response.message) {
                    this.limitDialog.nativeElement.open = true;
                    this.spinner.hide("spinnerMain");
                } else {
                    this.score = response.score;
                    this.percentile = response.percentile;
                    this.scoreDialog.nativeElement.open = true;
                    this.spinner.hide("spinnerMain");
                }
            });
        } else {
            this.warningDialog.nativeElement.open = true;
        }
    }
}
