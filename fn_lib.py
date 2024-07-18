import streamlit as st
import numpy as np


def get_data():
    x = np.linspace(0, 10, 100)
    y1 = np.random.randn(100)
    y2 = np.random.randn(100)
    y3 = np.random.randn(100)
    y4 = np.random.randn(100)
    return x, y1, y2, y3, y4



def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

