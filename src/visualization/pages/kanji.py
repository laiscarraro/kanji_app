import streamlit as st

def render_page(session):
    user = session.get_user()
    user_animes = user.get_animes_df()

    st.title('Priorização de Kanji')

    animes = st.multiselect(
        label='Selecione quais animes serão considerados na ordenação',
        options=user_animes.anime_name.values
    )
    