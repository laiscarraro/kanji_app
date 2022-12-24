import streamlit as st
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from st_aggrid import GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager

if st.session_state['user_found']:
    user = st.session_state['session'].get_user()

    st.title('Dicionário de Kanji')
    st.markdown('Saiba quais Kanji estudar primeiro para entender seus animes com mais facilidade. Marque na tabela abaixo quais Kanji você já conhece, para que eles sejam liberados em seus estudos. Após selecionar, clique em "Update". Você pode configurar as suas recomendações abaixo.')


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
        
    known_kanji = [i for i in user.get_kanji()]
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
        use_checkbox=True,
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
        update_mode=GridUpdateMode.MANUAL
    )

    selected = grid["selected_rows"]
    if len(selected) > 0:
        user.update_kanji(
            ''.join(
                [i['Kanji'] for i in selected]
            )
        )
        st.success('Kanjis conhecidos atualizados!')