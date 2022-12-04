import streamlit as st

def render_page(session):
    user = session.get_user()
    anime_subtitles = {
        anime.get_name(): anime.get_subtitles() 
        for anime in user.get_animes()
    }

    anime = st.selectbox(
        label='Selecione um anime para ver suas legendas',
        options=anime_subtitles.keys()
    )

    st.dataframe(anime_subtitles[anime])