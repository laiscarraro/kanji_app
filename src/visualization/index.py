import streamlit as st
from pages import home, subtitles, kanji, words, episodes
from modules import session

st.set_page_config(layout="wide")

session = session.Session()
user_login = st.text_input('Digite seu login')

if user_login != '':
    user_found = session.set_user(user_login)
    if user_found:
        tabs = st.tabs(['Home', 'Legendas', 'Kanji', 'Palavras', 'Episódios'])
        with tabs[0]:
            home.render_page(session)
        with tabs[1]:
            subtitles.render_page(session)
        with tabs[2]:
            kanji.render_page(session)
        with tabs[3]:
            words.render_page(session)
        with tabs[4]:
            episodes.render_page(session)
    else:
        st.warning('Não encontrei esse login :(')