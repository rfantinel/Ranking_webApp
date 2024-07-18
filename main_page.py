import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from fn_lib import navigate_to, get_data

class MainPage():
    def __init__(self, page_add_game, page_add_player) -> None:
        self.page_name = 'Personal Ranking'       
        
        self.page_add_game = page_add_game
        self.page_add_player = page_add_player
        self.page_logic()

    def page_logic(self):
        if 'page' not in st.session_state:
            st.session_state['page'] = self.page_name 

        # Logica di navigazione tra le pagine
        if st.session_state['page'] == self.page_name:
            self.show()
            
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
                

    def show(self):
        st.title(self.page_name)
        st.subheader('Ranking')

        if len(list(st.session_state.players_dict))>0:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            cmap = cm.viridis(np.arange(0, 255, step=int(256/len(list(st.session_state.players_dict)))))  # Scegli una colormap (esempio: viridis)

            for name in st.session_state.players_dict:
                if len(st.session_state.players_dict[name].n_game)>0:
                    idx = np.array(st.session_state.players_dict[name].idx)
                    n_game = np.array(st.session_state.players_dict[name].n_game)
                    mu = np.array(st.session_state.players_dict[name].ranking_mu)
                    sigma = np.array(st.session_state.players_dict[name].ranking_sigma)
                    
                    upper_bound = mu + 0.5*sigma
                    lower_bound = mu - 0.5*sigma
                    # st.line_chart(ranking_chart)
                    # Creare il grafico
                    ax.fill_between(n_game, lower_bound, upper_bound, color=cmap[idx, :], alpha=0.3)
                    if n_game.shape[0]==1:
                        ax.scatter(n_game, mu, label=name, color=cmap[idx, :],)
                    else:
                        ax.plot(n_game, mu, label=name, color=cmap[idx, :], marker='o')
            
                    ax.set_xlabel('N game')
                    ax.set_ylabel('Ranking')
            
            ax.legend()

            # Visualizzare il grafico in Streamlit
            st.pyplot(fig)

        if st.button("Create Game"):
            navigate_to(self.page_add_game.page_name)
        
        if st.button("Add New Player"):
            navigate_to(self.page_add_player.page_name)


       
