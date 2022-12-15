import streamlit as st
from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager

def render_page(session):
    st.title('Priorização de Kanji')

    user = session.get_user()
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

    st.dataframe(recommendation)

    