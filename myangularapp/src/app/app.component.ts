import { Component } from '@angular/core';
import { HaikuWriteComponent } from '@components/haiku-write.component';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [
    HaikuWriteComponent, 
    RouterModule, 
    HttpClientModule,
  ],
})
export class AppComponent {
  title = 'haiku.best';
}
