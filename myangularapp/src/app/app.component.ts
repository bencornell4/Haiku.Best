import { CUSTOM_ELEMENTS_SCHEMA, Component } from '@angular/core';
import { HelloWorldComponent } from '@components/hello-world.component';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [
    HelloWorldComponent, 
    RouterModule, 
    HttpClientModule, 
  ],
})
export class AppComponent {
  title = 'myreactapp';
}
