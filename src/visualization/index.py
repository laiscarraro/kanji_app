import streamlit as st
from pages import Home, Dicionário, Kanji, Leitura
from modules import session

st.set_page_config(layout="wide")

session = session.Session()
user_login = st.selectbox('Escolha o login', [
    'laiscarraro', 'pablito'
])

if user_login != '':
    user_found = session.set_user(user_login)
    if user_found:
        tabs = st.tabs(['Home', 'Dicionário', 'Kanji', 'Leitura'])
        with tabs[0]:
            Home.render_page(session)
        with tabs[1]:
            Dicionário.render_page(session)
        with tabs[2]:
            Kanji.render_page(session)
        with tabs[3]:
            Leitura.render_page(session)
    else:
        st.warning('Não encontrei esse login :(')