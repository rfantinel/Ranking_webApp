import streamlit as st
import json

import numpy as np
import pandas as pd

from ranking import Ranking




class NewGamePage():
    def __init__(self) -> None:
        self.page_name = 'Record New Game'
        self.main_page = None

    def create_page(self):
        st.title(self.page_name)

    
    def show(self):   
        players = list(st.session_state.players_dict)

        st.title('Create Game')

        if st.session_state.user_level ==2: 
            # Select Players for team A
            st.header('Winner/s')
            team_w = st.multiselect('Select winner player/s', players)

            # Rimuovi i giocatori selezionati per la Squadra A dalla lista per la Squadra B
            remaining_players = [player for player in players if player not in team_w]

            # Select Players for team B
            st.header('Loser/s')
            team_l = st.multiselect('Select loser player/s', remaining_players)

            remaining_players = [player for player in remaining_players if player not in team_l]

            # # Mostra le squadre
            # st.subheader('Team Winner:')
            # st.write(team_w)

            # st.subheader('Team Looser:')
            # st.write(team_l)

            # Verifica che non ci siano giocatori duplicati tra le squadre
            if len(set(team_w).intersection(set(team_l))) > 0:
                st.error("Error: Duplicated players in A and B teams!")
            else:
                if len(team_w)>0 and len(team_l)>0:
                    st.success("Game correctly created !")


                    if st.button("Add Game"):
                        
                        st.session_state.ranking.add_game(team_w, team_l, remaining_players)
                        
                        for name in team_w+team_l:
                            st.session_state.players_dict[name].n_game.append(st.session_state.ranking.n_game)
                            st.session_state.data[st.session_state.players_dict[name].complete_name] = st.session_state.players_dict[name].__dict__

                        for name in remaining_players:
                            st.session_state.data[st.session_state.players_dict[name].complete_name] = st.session_state.players_dict[name].__dict__
                    
                        # Salva il dizionario in un file JSON
                        with open(st.session_state.players_dict_file, 'w') as file:
                            json.dump(st.session_state.data, file, indent=4)

                        # update table
                            
        data = {}
        n_rows = 0
        for name in st.session_state.players_dict:
            if n_rows< len(st.session_state.players_dict[name].games):
                n_rows = len(st.session_state.players_dict[name].games)

            data[name] = st.session_state.players_dict[name].games

        for name in data:
            while len(data[name]) < n_rows:
                data[name].append(None)

        
       
        df = pd.DataFrame(data)

        if st.session_state.user_level ==2: 
            # Seleziona la riga da rimuovere
            rm_idx = st.text_input('remove row n:')

            # Pulsante per rimuovere la riga
            if st.button('remove row'):
                rm_idx_s = rm_idx.split('-')
                
                rm_idx_s0 = rm_idx_s[0]
                rm_idx_s1 = rm_idx_s[0]
                if len(rm_idx_s)>1:
                    rm_idx_s1 = rm_idx_s[1]
                    
                if int(rm_idx_s1) >= int(rm_idx_s0):  
            
                    for rm_idx in np.arange(int(rm_idx_s1), int(rm_idx_s0)-0.1, step=-1):
                        rm_idx = int(rm_idx)
                        if rm_idx >= 0 and rm_idx < len(df):
                            df = df.drop(index=rm_idx)
                            
                            for name in st.session_state.players_dict:
                                try:
                                    st.session_state.players_dict[name].games.pop(rm_idx)
                                except:
                                    aaaa = 0    
                                st.session_state.players_dict[name].mu = 1000
                                st.session_state.players_dict[name].sigma = 100
                                st.session_state.players_dict[name].ranking_mu = []
                                st.session_state.players_dict[name].ranking_sigma = []
                                rm_idx_2 = np.argwhere(np.array(st.session_state.players_dict[name].n_game)==rm_idx)
                                if rm_idx_2.shape[0]>0:
                                    # st.session_state.players_dict[name].n_game = st.session_state.players_dict[name].n_game[0:rm_idx_2[0][0]]+st.session_state.players_dict[name].n_game[rm_idx_2[0][0]+1:]
                                    st.session_state.players_dict[name].n_game.pop(rm_idx_2[0][0])
                                    for j in np.arange(rm_idx_2[0][0], len(st.session_state.players_dict[name].n_game)):
                                        st.session_state.players_dict[name].n_game[j] -=1
                                
                            new_ranking = st.session_state.ranking.recompute_all_ranking()
                            
                            for name in st.session_state.players_dict:
                                st.session_state.data[st.session_state.players_dict[name].complete_name] = st.session_state.players_dict[name].__dict__

                            st.session_state.ranking.n_game -= 1

                            # Salva il dizionario in un file JSON
                            with open(st.session_state.players_dict_file, 'w') as file:
                                json.dump(st.session_state.data, file, indent=4)

                            st.success(f'Row {rm_idx} removed successfully!')



                        else:
                            st.warning(f'Row {rm_idx} not valid.')

                data = {}
                n_rows = 0
                for name in st.session_state.players_dict:
                    if n_rows< len(st.session_state.players_dict[name].games):
                        n_rows = len(st.session_state.players_dict[name].games)

                    data[name] = st.session_state.players_dict[name].games

                for name in data:
                    while len(data[name]) < n_rows:
                        data[name].append(None)

                
            
                df = pd.DataFrame(data)
            # Aggiorna la tabella dopo la rimozione
        table = st.table(df)