import streamlit as st
import json

import numpy as np 
import pandas as pd

from player import Player

from fn_lib import find_last_not_none, count_not_none


class NewPlayerPage():
    def __init__(self) -> None:
        self.page_name = 'Add New Player'
        self.main_page = None
    
    def create_page(self):
        st.title(self.page_name)

    # Pagina Pag.p2
    def show(self):
       

        st.title('Add Player')

        if st.session_state.user_level ==2: 
            input_name = st.text_input("*name:")
            input_surname = st.text_input("surname:")


            if input_name:
                st.write("name updated")
            else:
                st.write("*Please insert the name of the new player")

            if input_surname:
                st.write(f"surname updated")

            if st.button("Add Player"):
                if input_name!='' and input_surname!='':
                    new_player = Player( len(list(st.session_state.players_dict)), input_name, input_surname)
                    if not new_player.complete_name in st.session_state.players_dict:
                        st.session_state.players_dict[new_player.complete_name] = new_player
                    else:
                        idx = 1
                        new_player = Player( len(list(st.session_state.players_dict)), input_name, input_surname + ' ' + str(idx))
                        while new_player.complete_name in st.session_state.players_dict:
                            idx += 1
                            new_player = Player( len(list(st.session_state.players_dict)), input_name, input_surname + ' ' + str(idx))
                            
                        st.session_state.players_dict[new_player.complete_name] = new_player
                        
                    st.session_state.data[new_player.complete_name] = new_player.__dict__
                    # Salva il dizionario in un file JSON
                    with open(st.session_state.players_dict_file, 'w') as file:
                        json.dump(st.session_state.data, file, indent=4)
                    

                    st.write('player "'+ str(new_player.complete_name), '" added to players list')



            inv_list = ["..."]
            for i, i_list in enumerate(list(st.session_state.players_dict)):
                inv_list.append(list(st.session_state.players_dict)[len(list(st.session_state.players_dict))-i-1])
            

            selected_name = st.selectbox('Select player to remove:', inv_list)
            if st.button("Remove Player"):
                if selected_name in list(st.session_state.players_dict):

                    del st.session_state.players_dict[selected_name]
                    del st.session_state.data[selected_name]

                    # Salva il dizionario in un file JSON
                    with open(st.session_state.players_dict_file, 'w') as file:
                        json.dump(st.session_state.data, file, indent=4)

                    st.success(f'{selected_name} removed!')


                else:
                    st.error('Name selected not in list.')
                
                st.rerun()

       

        data = {}
        df_cols_name = ['Total games', 'Played games', 'Won', 'Lost', 'Won [%]', 'Lost [%]', 'Best score', 'Score']
        for name in st.session_state.players_dict:

            idx_last_played_game = find_last_not_none(st.session_state.players_dict[name].games)
            N_played_game = int(count_not_none(st.session_state.players_dict[name].games))

            games_lost =  np.sum(np.array(st.session_state.players_dict[name].games)==0)
            games_won =  np.sum(np.array(st.session_state.players_dict[name].games)==1)

            Tot_games = len(st.session_state.players_dict[name].games)

            if len(st.session_state.players_dict[name].n_game) > 0:    
                last_played_game = st.session_state.players_dict[name].n_game[idx_last_played_game]
            else:
                Tot_games = 0
                last_played_game = None
                
            last_score = st.session_state.players_dict[name].mu
            best_score = last_score
            if len(st.session_state.players_dict[name].n_game) > 0:
                best_score = np.max(np.array(st.session_state.players_dict[name].ranking_mu))
            
            data[name] = [Tot_games, N_played_game, games_won, games_lost, games_won/N_played_game*100, games_lost/N_played_game*100,  best_score, last_score]
           

        df = pd.DataFrame(data).transpose()
        df = df.set_axis(df_cols_name, axis=1)
        df_sorted = df.sort_values(by=df_cols_name[-1], ascending=False)


        st.dataframe(df_sorted, height=250, use_container_width=True)

