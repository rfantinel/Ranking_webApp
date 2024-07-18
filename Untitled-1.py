
import streamlit as st

# Funzione di navigazione tra le pagine
def navigate_to(page):
    st.session_state['page'] = page
    st.rerun()

# Imposta lo stato iniziale della sessione
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

# Logica di navigazione tra le pagine
if st.session_state['page'] == 'main':
    st.title("Pagina Principale")
    if st.button("Vai alla Pagina Secondaria"):
        navigate_to('secondary')
elif st.session_state['page'] == 'secondary':
    st.title("Pagina Secondaria")
    if st.button("Torna alla Pagina Principale"):
        navigate_to('main')

# # Opzioni per allineare le pagine a destra (richiede un layout personalizzato)
# st.markdown(
#     """
#     <style>
#     .main {
#         display: flex;
#         justify-content: flex-end;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
