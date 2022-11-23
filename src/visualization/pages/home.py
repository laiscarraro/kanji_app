import streamlit as st
import pandas as pd

def render_page(user):
    user_name = user.user_name.values[0]
    st.markdown('## Bem-vindo/a, ' + user_name + '!')

    user_anime = pd.read_csv('data/user_anime.csv', sep=';')
    animes = pd.read_csv('data/anime.csv', sep=';')

    user_animes = pd.merge(
        user_anime[user_anime.user_id == user.user_id], 
        animes, on='anime_id'
    )

    st.markdown('Você tem ' + str(len(user_animes)) + ' animes.')

    st.dataframe(user_animes)
    