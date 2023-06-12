import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { FastApiService } from '../fast-api.service';
import { Router } from "@angular/router"
import { FormGroup, FormBuilder,FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  loginForm: FormGroup;

  constructor(private navCtrl: NavController, private fastApiService: FastApiService, private router: Router, private formBuilder: FormBuilder) {
    this.loginForm = this.formBuilder.group({
      username: new FormControl('', Validators.compose([
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(20),
        Validators.nullValidator
      ])),
      password: new FormControl('', Validators.compose([
        Validators.required,
        Validators.minLength(4),
        Validators.maxLength(20),
        Validators.nullValidator
      ]))
    });
  }

  login() {
      this.fastApiService.loginUser(this.loginForm.value.username, this.loginForm.value.password).subscribe(
        (response) => {

        }
      );
  }

  ngOnInit() {
    // Habilitar o botão de login quando o formulário for válido
    const loginButton = document.querySelector('#login-button') as HTMLButtonElement;
    this.loginForm.valueChanges.subscribe(() => {
      if (this.loginForm.valid) {
        loginButton.disabled = false;
      } else {
        loginButton.disabled = true;
      }
    });
  }
}