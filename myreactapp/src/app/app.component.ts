import { Component } from '@angular/core';
import { HelloWorldComponent } from '@components/hello-world.component';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  imports: [HelloWorldComponent, RouterModule],
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'myreactapp';
}
