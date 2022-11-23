import streamlit as st
import pandas as pd

from pages import home

st.set_page_config(layout="wide")

users = pd.read_csv('data/user.csv', sep=';')
user_login = st.text_input('Digite seu login')

try:
    user = users[users.user_login == user_login]
except:
    user = None
    st.warning('Usuário não encontrado')

if user_login != '' and user is not None:
    tabs = st.tabs(['Home'])
    with tabs[0]:
        home.render_page(user)