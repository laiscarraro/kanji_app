import streamlit as st
from modules.session import Session
from modules.greeter import Greeter
from modules.managers.anime_manager import AnimeManager

st.set_page_config(layout="wide")

if 'session' not in st.session_state:
    st.session_state['session'] = Session()

if 'user_found' not in st.session_state:
    st.session_state['user_found'] = False

user_login = st.selectbox('Escolha o login', [
    'laiscarraro', 'pablito'
])

if user_login != '':
    user_found = st.session_state['session'].set_user(user_login)
    if user_found:
        st.session_state['user_found'] = True
    else:
        st.warning('Não encontrei esse login :(')

if st.session_state['user_found']:
    greeter = Greeter()
    user = st.session_state['session'].get_user()
    user_animes = user.get_animes_df()

    st.markdown('## ' + greeter.greet(user))
    st.markdown('Você tem ' + str(user.count_animes()) + ' animes.')

    st.dataframe(user_animes)

    with st.expander('Adicionar animes'):
        manager = AnimeManager(user)
        available = manager.get_available_animes()

        new_anime = st.selectbox(
            label='Selecione o anime que você quer adicionar',
            options=available.anime_id.values,
            format_func=(
                lambda id: available[
                    available.anime_id == id
                ].anime_name.values[0]
            )
        )

        if st.button('Adicionar'):
            manager.add_anime(new_anime)
            st.experimental_rerun()

    if user.count_animes() > 0:
        with st.expander('Remover animes'):
            manager = AnimeManager(user)

            old_anime = st.selectbox(
                label='Selecione o anime que você quer remover',
                options=user_animes.id.values,
                format_func=(
                    lambda id: user_animes[
                        user_animes.id == id
                    ].name.values[0]
                )
            )

            if st.button('Remover'):
                manager.remove_anime(old_anime)
                st.experimental_rerun()
