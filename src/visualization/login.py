import streamlit as st
import streamlit_authenticator as stauth
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
