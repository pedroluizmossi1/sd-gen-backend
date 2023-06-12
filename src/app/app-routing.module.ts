import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './auth.guard';
import { MenuComponent } from './menu/menu.component';
import { InformacoesComponent } from './menu/informacoes/informacoes.component';

const routes: Routes = [
  {path: 'login',loadChildren: () => import('./login/login.module').then( m => m.LoginPageModule)},
  {path: 'tabs',loadChildren: () => import('./tabs/tabs.module').then( m => m.TabsPageModule),canActivate: [AuthGuard]},
  {path: '',redirectTo: 'login',pathMatch: 'full'},
  { path: 'menu', component: MenuComponent, children: [
    { path: 'informacoes', component: InformacoesComponent }
  ]},
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
