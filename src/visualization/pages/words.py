import streamlit as st

def render_page(session):
    user = session.get_user()

    st.title('Palavras')