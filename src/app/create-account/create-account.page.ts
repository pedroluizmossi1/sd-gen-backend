import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder,FormControl, Validators } from '@angular/forms';
import { FastApiService } from '../fast-api.service';

@Component({
  selector: 'app-create-account',
  templateUrl: './create-account.page.html',
  styleUrls: ['./create-account.page.scss'],
})
export class CreateAccountPage implements OnInit {
  registerForm: FormGroup;

  constructor(private formBuilder: FormBuilder, private fastApiService: FastApiService ) { 
    this.registerForm = this.formBuilder.group({
      'username': ['', Validators.compose([
        Validators.required,
        Validators.minLength(4),
        Validators.maxLength(20),
        Validators.nullValidator])],
      'password': ['', Validators.compose([
        Validators.required,
        Validators.minLength(6),
        Validators.maxLength(20),
        Validators.nullValidator])],
      'confirmPassword': ['', Validators.compose([
        Validators.required,
        Validators.minLength(6),
        Validators.maxLength(20),
        Validators.nullValidator])],
      'email': ['', Validators.compose([
        Validators.required,
        Validators.email,
        Validators.minLength(4),
        Validators.maxLength(50),
        Validators.nullValidator])],
      'firstName': ['', Validators.compose([
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(30),
        Validators.nullValidator])],
      'lastName': ['', Validators.compose([
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(30),
        Validators.nullValidator])],
    });
  }

  register() {
    this.fastApiService.registerUser(this.registerForm.value.username, this.registerForm.value.password, this.registerForm.value.email, this.registerForm.value.firstName, this.registerForm.value.lastName).subscribe(
      (response) => {
        console.log(response);
      }
    );
  }
    

  ngOnInit() {
    const registerButton = document.querySelector('#register-button') as HTMLButtonElement;
    this.registerForm.valueChanges.subscribe(() => {
      if (this.registerForm.valid) {
        registerButton.disabled = false;
      } else {
        registerButton.disabled = true;
      }
    }
    );
  }

}
