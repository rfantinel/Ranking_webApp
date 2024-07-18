import streamlit as st
import json

from player import Player

class NewPlayerPage():
    def __init__(self) -> None:
        self.page_name = 'Add New Player'
        self.main_page = None
    
    def create_page(self):
        st.title(self.page_name)

    # Pagina Pag.p2
    def show(self):
       

        st.title('Add Player')

        
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



        self.player_list = st.selectbox('players list:', list(st.session_state.players_dict))
       
       