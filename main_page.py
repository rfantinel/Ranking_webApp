import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from fn_lib import navigate_to, get_data

class MainPage():
    def __init__(self, page_add_game, page_add_player, page_user_level_settings) -> None:
        self.page_name = 'Personal Ranking'       
        
        self.col1, self.col2, self.col3 = st.columns([0.8, 0.1, 0.1])

        self.page_user_level_settings = page_user_level_settings
        self.page_add_game = page_add_game
        self.page_add_player = page_add_player
        
        self.page_logic()

    def page_logic(self):
        if 'page' not in st.session_state:
            st.session_state['page'] = self.page_name 

        # Logica di navigazione tra le pagine
        if st.session_state['page'] == self.page_name:
            self.show()
        
        elif st.session_state['page'] == self.page_user_level_settings.page_name:
            self.page_user_level_settings.main_page = self
            self.page_user_level_settings.show()

            if st.button("Torna alla Pagina Principale"):
                navigate_to(self.page_name)

        elif st.session_state['page'] == self.page_add_player.page_name:
            self.page_add_player.main_page = self
            self.page_add_player.show()

            if st.button("Torna alla Pagina Principale"):
                navigate_to(self.page_name)

        elif st.session_state['page'] == self.page_add_game.page_name:
            self.page_add_game.main_page = self
            self.page_add_game.show()

            if st.button("Torna alla Pagina Principale"):
                navigate_to(self.page_name)
                
    def show_settings_icon(self):
        if st.session_state['page'] == self.page_name:
            st.markdown("""
                <style>
                .settings-button {
                    background-color: transparent;
                    border: none;
                    color: #007bff;
                    font-size: 24px;
                    cursor: pointer;
                }

                .settings-button:hover {
                    color: #0056b3;
                }

                .settings-button:focus {
                    outline: none;
                }
                </style>
                """, unsafe_allow_html=True)


    def show(self):
        st.title(self.page_name)
        st.subheader('Ranking')

        with self.col3:
            # Mostra l'icona di impostazioni
            self.show_settings_icon()

            if st.button("⋮", key="settings", help="Impostazioni"):
                navigate_to(self.page_user_level_settings.page_name)



        if len(list(st.session_state.players_dict))>0:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            if len(list(st.session_state.players_dict))<=12:
                cmap = cm.get_cmap('Set1', 10).colors
                # cmap = cm.get_cmap('tab10', 10).colors
            elif len(list(st.session_state.players_dict))>12:
                cmap = cm.get_cmap('tab20', 20).colors
            elif len(list(st.session_state.players_dict))>20:
                cmap = cm.jet(np.arange(0, 255, step=int(256/len(list(st.session_state.players_dict)))))  # Scegli una colormap (esempio: viridis)
         
            # cmap = cm.jet(np.arange(0, 255, step=int(256/len(list(st.session_state.players_dict)))))  # Scegli una colormap (esempio: viridis)

            for name in st.session_state.players_dict:
                if type(st.session_state.players_dict[name].n_game)==int:
                    st.session_state.players_dict[name].n_game = [st.session_state.players_dict[name].n_game]
                if len(st.session_state.players_dict[name].n_game)>0:
                    idx = np.array(st.session_state.players_dict[name].idx)
                    n_game = np.array(st.session_state.players_dict[name].n_game)
                    mu = np.array(st.session_state.players_dict[name].ranking_mu)
                    sigma = np.array(st.session_state.players_dict[name].ranking_sigma)
                    
                    upper_bound = mu + 0.5*sigma
                    lower_bound = mu - 0.5*sigma
                    # st.line_chart(ranking_chart)
                    # Creare il grafico
                    ax.fill_between(n_game, lower_bound, upper_bound, color=cmap[idx, :], alpha=0.2)
                    if n_game.shape[0]==1:
                        ax.scatter(n_game, mu, label=name, color=cmap[idx, :],)
                    else:
                        ax.plot(n_game, mu, label=name, color=cmap[idx, :], marker='o')
            
                    ax.set_xlabel('N game')
                    ax.set_ylabel('Ranking')
            
            ax.legend()

            # Visualizzare il grafico in Streamlit
            st.pyplot(fig)

        if st.button("Games"):
            navigate_to(self.page_add_game.page_name)
        
        if st.button("Players"):
            navigate_to(self.page_add_player.page_name)


       
