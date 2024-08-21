import streamlit as st
import json

import numpy as np
import pandas as pd

from ranking import Ranking




class UserLevelSettingPage():
    def __init__(self) -> None:
        self.page_name = 'User Level Setting'
        self.main_page = None
        self.admin_pwd = 'pwd123'

        # Stato iniziale: livello di visualizzazione
        if 'error_level' not in st.session_state:
            st.session_state.error_level = 0
        if 'show_settings' not in st.session_state:
            st.session_state.show_settings = False
        if 'temp_level' not in st.session_state:
            st.session_state.temp_level = st.session_state.user_level

    def create_page(self):
        st.title(self.page_name)

    
    def show(self):   
        st.write("### Change user level")

        # Mostra il radio button per selezionare il livello
        st.session_state.temp_level = st.radio(
            "Select level:", 
            [1, 2], 
            index=st.session_state.temp_level - 1
        )
        
        if st.session_state.temp_level == 2:
            password = st.text_input("Insert password:", type="password")
            if st.button("Confirm passowrd"):
                if password == self.admin_pwd:
                    st.session_state.user_level = 2
                    st.session_state.temp_level = 2
                    st.success("Admin user level activated.")
                else:
                    st.session_state.user_level = 1
                    st.session_state.temp_level = 1
                    st.session_state.error_level = 1
                    st.rerun()

        else:
            st.session_state.user_level = 1
            st.session_state.temp_level = 1
            if st.session_state.error_level == 1:
                st.error("Wrong password! Default user level activated.")
                st.session_state.error_level = 0

            st.success("Default user level activated.")

        aaaa = 0