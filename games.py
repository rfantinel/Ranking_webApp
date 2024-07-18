
class Games():
    def __init__(self, players) -> None:
        self.time = []
        self.n_absolute = []
        self.teams = []
        self.team_winner = []
        self.players = players
    
    def add_game(self, n_absolute, time, teams, team_winner):
        self.time.append(time)
        self.n_absolute.append(n_absolute)
        self.teams.append(teams)
        self.team_winner.append(team_winner)
        self.update_players_ranking()

    def update_players_ranking(self):

        for i, t_i in enumerate(self.teams[-1]):
            for p in t_i:
                if i == self.team_winner[-1]:
                    p.add_game_played(self.n_absolute[-1], self.time, self.teams[-1], 1)
                else:
                    p.add_game_played(self.n_absolute[-1], self.time, self.teams[-1], -1)                
        

        