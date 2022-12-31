import streamlit as st
from st_aggrid import AgGrid
from st_aggrid import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from src.visualization.login import initialize_page

if initialize_page():
    user = st.session_state['session'].get_user()

    st.title('Dicionário de Kanji')
    st.markdown('Saiba quais Kanji estudar primeiro para entender seus animes com mais facilidade. Na tabela abaixo, estão marcados os Kanji que você já conhece, segundo o seu deck do Anki. Estude mais Kanji para que eles sejam liberados em seus estudos! Você pode configurar as suas recomendações abaixo.')


    user_animes = user.get_animes_df()
    recommender = KanjiRecommendationManager(user)
    recommendation = recommender.get_latest_model()

    with st.expander('Configurar recomendações'):
        anime_ids = st.multiselect(
            label='Selecione quais animes serão considerados na recomendação',
            options=user_animes.id.values,
            format_func=(
                lambda id: user_animes[
                    user_animes.id == id
                ].name.values[0]
            ),
            default=user_animes.id.values
        )
        
        features = st.multiselect(
            label='Selecione quais variáveis serão utilizadas para criar a ordenação',
            options=recommender.handler.get_possible_features(),
            default=recommender.handler.get_possible_features()
        )

        if st.button('Aplicar alterações'):
            recommender.update_latest_model(
                anime_ids, features
            )
            recommendation = recommender.get_latest_model()
        
    known_kanji = st.session_state['anki_manager'].get_unlocked_kanji()
    kanji_index = recommendation[
        recommendation.Kanji.isin(known_kanji)
    ].index.tolist()

    gd = GridOptionsBuilder.from_dataframe(
        recommendation[[
            'Kanji', 'Suggested Order', 'Meaning',
            'Kunyomi', 'Onyomi'
        ]]
    )

    gd.configure_selection(
        selection_mode='multiple',
        suppressRowDeselection=True,
        suppressRowClickSelection=True,
        use_checkbox=False,
        pre_selected_rows=kanji_index
    )
    gd.configure_pagination(
        enabled=True, 
        paginationAutoPageSize=False,
        paginationPageSize=15
    )
    options = gd.build()
    
    grid = AgGrid(
        recommendation[[
            'Kanji', 'Suggested Order', 'Meaning',
            'Kunyomi', 'Onyomi'
        ]],
        gridOptions=options,
        update_mode=GridUpdateMode.NO_UPDATE,
        theme='alpine'
    )