import streamlit as st
from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.word_order import WordOrder

def render_page(session):
    user = session.get_user()
    user_animes = user.get_animes()
    recommender = KanjiRecommendationManager(user)
    kanji_order = recommender.get_latest_model()

    word_order = WordOrder(
        kanji_order,
        recommender.unified_subtitles
    )

    st.title('Palavras')

    st.dataframe(word_order.get_topological_order())