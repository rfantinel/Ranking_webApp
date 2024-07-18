import numpy as np
import copy


class Ranking():
    def __init__(self, players) -> None:
        self.players = players
        self.n_game = self.compute_n_games_playes()

    def compute_n_games_playes(self):
        return len(self.players[list(self.players)[0]].games)-1


    def recompute_all_ranking(self):
        players2 = copy.deepcopy(self.players)
        
        n_game_max = 0
        for name in players2:
            self.players[name].games = []
            if len(players2[name].n_game) >0:
                if n_game_max<players2[name].n_game[-1]:
                    n_game_max = players2[name].n_game[-1]
        
        for i_g in range(n_game_max+1):
            team_A = []
            team_B = []
            unassigned = []
            for name in players2:
                if i_g in players2[name].n_game:
                    idx = np.argwhere(np.array(players2[name].n_game) == i_g)[0][0]
                    if players2[name].games[idx] == 1:
                        team_A.append(name)
                    elif players2[name].games[idx] == 0:
                        team_B.append(name)
                    else:
                        unassigned.append(name)

            self.add_game(team_A, team_B, unassigned)
            self.n_game -= 1


    def prob_win(self, score_A, score_B):
        return 1 / (1 + np.exp(-(score_A - score_B)))

    # Funzione per aggiornare la distribuzione di un giocatore
    def update_ranking(self, mu_prior, sigma_prior, individual_contribution, sigma_D):
        # Calcola il fattore di guadagno
        K = sigma_prior**2 / (sigma_prior**2 + sigma_D**2)
        
        # Calcola il punteggio di riferimento R per il singolo giocatore
        R = individual_contribution
        
        # Aggiorna la media a posteriori
        mu_post = mu_prior + K * R
        
        # Aggiorna la varianza a posteriori
        sigma_post = sigma_prior * np.sqrt(1 - K)
        
        return mu_post, sigma_post


        
    def add_game(self, team_A, team_B, unassigned_players, lambda_penalty=900, sigma_D=400, win_contrib=100):
        # Parametri iniziali
        # lambda_penalty : Penalità per numero di giocatori
        # sigma_D : Varianza della differenza di punteggio
        score_A = 0
        mu_A = []

        for player in team_A:
            self.players[player].games.append(1)
            score_A += self.players[player].mu
            mu_A.append(self.players[player].mu)
        score_A -= lambda_penalty * len(team_A)
        mu_A = np.mean(np.array(mu_A))

        score_B = 0
        mu_B = []
        for player in team_B:
            self.players[player].games.append(0)
            score_B += self.players[player].mu
            mu_B.append(self.players[player].mu)
        score_B -= lambda_penalty * len(team_B)
        mu_B = np.mean(np.array(mu_B))

        for player in unassigned_players:
            self.players[player].games.append(None)
       
        score_diff = abs(score_A - score_B)
        mu_X = (mu_A+mu_B)/2

        # Aggiornamento dei ranking per ogni giocatore
        for player in team_A+team_B:
            mu_prior = self.players[player].mu
            sigma_prior = self.players[player].sigma
            
            # Contributo individuale del giocatore alla differenza di punteggio
            if player in team_A:
                individual_contribution = (3*score_diff - 0*(mu_A - self.players[player].mu) + (mu_X - self.players[player].mu)) + win_contrib
            else:
                individual_contribution = (-3*score_diff + 0*(mu_B - self.players[player].mu) - (mu_X - self.players[player].mu)) - win_contrib    
            
            
            mu_post, sigma_post = self.update_ranking(mu_prior, sigma_prior, individual_contribution, sigma_D)
            
            self.players[player].mu = mu_post
            self.players[player].sigma = sigma_post

            self.players[player].ranking_mu.append(mu_post)      
            self.players[player].ranking_sigma.append(sigma_post)

        self.n_game += 1