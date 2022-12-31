import streamlit as st
from modules.greeter import Greeter
from modules.managers.anime_manager import AnimeManager
from src.visualization.login import initialize_page

if initialize_page():
    greeter = Greeter()
    user = st.session_state['session'].get_user()
    user_animes = user.get_animes_df()

    st.markdown('## ' + greeter.greet(user))
    
    tabs = st.tabs(['Estatísticas', 'Configurar animes', 'Configurar decks do Anki'])

    with tabs[0]:
        st.write('Em construção :)')

    with tabs[1]:
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
    
    with tabs[2]:
        anki_manager = st.session_state['anki_manager']
        user_decks = anki_manager.get_user_decks()

        st.write('Você tem ' + str(len(user_decks)) + ' decks.')
        st.dataframe(user_decks)

        with st.expander('Editar decks'):
            kanji_decks = st.multiselect(
                'Escolha seus decks de Kanji',
                options=anki_manager.get_available_decks(),
                default=anki_manager.get_kanji_decks()
            )
            word_decks = st.multiselect(
                'Escolha seus decks de Palavras',
                options=anki_manager.get_available_decks(),
                default=anki_manager.get_word_decks()
            )
            if st.button('Atualizar'):
                if (
                    anki_manager.set_kanji_decks(kanji_decks) and
                    anki_manager.set_word_decks(word_decks)
                ):
                    st.experimental_rerun()
