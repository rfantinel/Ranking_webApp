import hashlib
import time

class Player():
    def __init__(self, idx, name, surname='') -> None:

        self.idx = idx

        self.name = name
        self.surname = surname
        self.id = self.generate_hashcode() 
        
        self.games = []
        self.n_game = []
        self.ranking_score = []
        
        self.mu = 1000
        self.sigma = 100
        self.ranking_mu = []
        self.ranking_sigma = []
        
        self.complete_name = name + ' ' + surname


    def add_game_played(self, n_absolute, time, teams, winner):
        self.games.time.append(time)
        self.teams_belongin.append(teams)
        self.games.n_game.append(n_absolute)

        self.ranking_score.append(self.ranking_score[-1] + winner)


    def generate_hashcode(self):
        hash_object = hashlib.sha256()
        hash_object.update(str(time.time()).encode('utf-8'))
        return hash_object.hexdigest()

