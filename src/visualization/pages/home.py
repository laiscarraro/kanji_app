import streamlit as st
import pandas as pd

def render_page(session):
    user = session.get_user()

    st.markdown('## Bem-vindo/a, ' + user.get_name() + '!')
    st.markdown('Você tem ' + user.count_animes() + ' animes.')

    st.dataframe(user.get_animes_df())

    with st.expander('Adicionar animes'):
        available_animes = pd.read_csv('data/animes.csv', sep=';')
        st.write(available_animes[
            ~available_animes.anime_id.isin(
                user.get_animes_df().id
            )
        ])
