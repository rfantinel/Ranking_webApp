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

def find_last_not_none(lst):
    count = 0
    for i, item in enumerate(lst):
        if item is not None:
            count = i
    return count


def count_not_none(lst):
    count = 0
    for item in lst:
        if item is not None:
            count += 1
    return count
