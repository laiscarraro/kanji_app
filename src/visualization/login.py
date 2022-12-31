import streamlit as st
import streamlit_authenticator as stauth
from modules.session import Session
from modules.managers.anki_manager import AnkiManager
import yaml

with open('src/visualization/config.yaml') as file:
    config = yaml.load(file, Loader=stauth.SafeLoader)

def make_login():
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login('Login', 'main')
    st.session_state["authetication_status"] = authentication_status

    if st.session_state["authetication_status"]:
        authenticator.logout('Logout', 'main')
        return username
    elif st.session_state["authentication_status"] == None:
        st.warning('Por favor, preencha os campos')
    else:
        st.error('Credenciais inválidas')

def initialize_page():
    st.set_page_config(layout="wide")

    if 'session' not in st.session_state:
        st.session_state['session'] = Session()
    if 'user_found' not in st.session_state:
        st.session_state['user_found'] = False
    if 'authetication_status' not in st.session_state:
        st.session_state['authetication_status'] = None
    if 'anki_manager' not in st.session_state:
        st.session_state['anki_manager'] = None

    if not st.session_state['user_found']:
        user_login = make_login()

        if user_login is not None:
            user_found = st.session_state['session'].set_user(user_login)
            if user_found:
                st.session_state['user_found'] = True
                st.session_state['anki_manager'] = AnkiManager(user_login)
    
    return st.session_state['user_found']