import { Component, OnInit } from '@angular/core';
import { FastApiService } from '../fast-api.service';
import { FormGroup, FormBuilder,FormControl, Validators } from '@angular/forms';
import { LoadingController } from '@ionic/angular';


@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.page.html',
  styleUrls: ['./user-profile.page.scss'],
})
export class UserProfilePage implements OnInit {

  user = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    is_active: false,
  };
  userProfileForm: FormGroup;

  constructor(private fastApiService: FastApiService, private formBuilder: FormBuilder, private loadingController: LoadingController) { 
    this.userProfileForm = this.formBuilder.group({
      'email': new FormControl('', Validators.compose([
        Validators.required,
        Validators.email,
        Validators.minLength(4),
        Validators.maxLength(50),
        Validators.nullValidator
      ])),
      'first_name': new FormControl('', Validators.compose([
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(30),
        Validators.nullValidator
      ])),
      'last_name': new FormControl('', Validators.compose([
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(30),
        Validators.nullValidator
      ])),
    });
    
  }
  
  getUserProfile() {
    this.fastApiService.getUserProfile().subscribe(
      (response) => {
        this.user.username = response.login;
        this.user.email = response.email;
        this.user.first_name = response.first_name;
        this.user.last_name = response.last_name;

        this.userProfileForm.setValue({
          email: this.user.email,
          first_name: this.user.first_name,
          last_name: this.user.last_name
        });
      }
    );
  }

  async updateUserProfile() {
    const loading = await this.loadingController.create({
      message: 'Updating profile...'
    });
    await loading.present();
  
    this.fastApiService.updateUserProfile(this.userProfileForm.value.email, this.userProfileForm.value.first_name, this.userProfileForm.value.last_name).subscribe(
      (response) => {
        this.user.email = this.userProfileForm.value.email;
        this.user.first_name = this.userProfileForm.value.first_name;
        this.user.last_name = this.userProfileForm.value.last_name;
  
        loading.dismiss();
      },
      (error) => {
        console.error(error);
        loading.dismiss();
      }
    );
  }

  loadingPresented = false;

  openLoading() {
    this.loadingPresented = true;
  }

  ngOnInit() {
    this.getUserProfile();
  }

}
