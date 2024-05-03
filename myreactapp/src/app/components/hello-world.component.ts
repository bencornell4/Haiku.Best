import { Component } from "@angular/core";

@Component({
    standalone: true,
    selector: 'app-hello-world',
    templateUrl: './hello-world.component.html'
})

export class HelloWorldComponent {
    message: string = 'Hello, World!';
}