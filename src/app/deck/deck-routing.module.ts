import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DeckComponent } from './deck.component';

const routes: Routes = [{ path: '', component: DeckComponent },
  { path: 'game', loadChildren: () => import('./game/game.module').then(m => m.GameModule) },];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DeckRoutingModule { }
