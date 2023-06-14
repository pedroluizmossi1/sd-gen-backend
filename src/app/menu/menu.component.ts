import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FastApiService } from '../fast-api.service';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
})
export class MenuComponent  implements OnInit {

  constructor(private fastApiService: FastApiService ) { }

  logout() {
    this.fastApiService.logoutUser().subscribe(
      (response) => {
        
      }
    );
  }

  ngOnInit() {
  }

}
