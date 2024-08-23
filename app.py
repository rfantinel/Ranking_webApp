import os


import streamlit as st
import numpy as np


import json

from player import Player
from games import Games

from main_page import MainPage
from new_player_page import NewPlayerPage
from new_game_page import NewGamePage
from user_level_setting_page import UserLevelSettingPage
from ranking import Ranking



# Pagina principale
def main():

    if 'players_dict_file' not in st.session_state:
        st.session_state.players_dict_file = 'players_dict.json'
       

    # Leggi il contenuto esistente del file JSON
    if os.path.exists(st.session_state.players_dict_file):
        try:
            with open(st.session_state.players_dict_file, 'r') as file:
                data = json.load(file)
        except:
            data = {}
    else:
        data = {}

    if 'data' not in st.session_state:
        st.session_state.data = data

    n_game = 0
    if 'players_dict' not in st.session_state:
        st.session_state.players_dict = {}
        if len(list(data))>0:
            for pl in data:
                player_saved = Player( data[pl]['idx'], data[pl]['name'], data[pl]['surname'])
                player_saved.games = data[player_saved.complete_name]['games']
                player_saved.id = data[player_saved.complete_name]['id']
                player_saved.n_game = data[player_saved.complete_name]['n_game']
                player_saved.ranking_score = data[player_saved.complete_name]['ranking_score']
                player_saved.ranking_mu = data[player_saved.complete_name]['ranking_mu']
                player_saved.ranking_sigma = data[player_saved.complete_name]['ranking_sigma']
                player_saved.mu = data[player_saved.complete_name]['mu']
                player_saved.sigma = data[player_saved.complete_name]['sigma']
                st.session_state.players_dict[player_saved.complete_name] = player_saved

    if 'games_obj' not in st.session_state:
        st.session_state.games_obj = Games(st.session_state.players_dict)

    
    if 'ranking' not in st.session_state:
        st.session_state.ranking = Ranking(players=st.session_state.players_dict)

    if 'user_level' not in st.session_state:
            st.session_state.user_level = 1


    user_level_settings = UserLevelSettingPage()
    new_player_pg_obj = NewPlayerPage()
    new_game_pg_obj = NewGamePage()
    main_pg_obj = MainPage(new_game_pg_obj, new_player_pg_obj, user_level_settings)


 


# Avvio dell'app
if __name__ == '__main__':
    main()






