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
    # Iterate over the list in reverse
    for item in reversed(lst):
        if item is not None:
            return item
    return None  # Return None if all elements are None

def count_not_none(lst):
    count = 0
    for item in lst:
        if item is not None:
            count += 1
    return count
