import streamlit as st
import pandas as pd

from modules.greeter import Greeter

def render_page(session):
    greeter = Greeter()
    user = session.get_user()

    st.markdown('## ' + greeter.greet(user))
    st.markdown('Você tem ' + str(user.count_animes()) + ' animes.')

    st.dataframe(user.get_animes_df())

    with st.expander('Adicionar animes'):
        available_animes = pd.read_csv('data/animes.csv', sep=';')
        st.write(available_animes[
            ~available_animes.anime_id.isin(
                user.get_animes_df().id
            )
        ])
