import streamlit as st

from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.content_dependencies import ContentDependencies
from modules.models.study_order import StudyOrder

import gtts
from googletrans import Translator

def render_page(session):
    st.title('Palavras')
    st.write('王様ランキングとは')

    user = session.get_user()
    recommender = KanjiRecommendationManager(user)
    kanji_order = recommender.get_latest_model()
    
    n_unlocked_kanji = st.text_input('Quantos Kanji da lista você já estudou?')

    if n_unlocked_kanji != '':
        n_unlocked_kanji = int(n_unlocked_kanji)
        unlocked_kanji = kanji_order.iloc[:n_unlocked_kanji]

        dependencies = ContentDependencies(user.get_unified_subtitles())
        study = StudyOrder(unlocked_kanji, dependencies, kanji_order)
        sentences = study.get_unlocked_sentences()

        if len(sentences) == 0:
            st.warning('Nenhuma frase para estes Kanji! Tente estudar mais um, ou adicionar mais animes.')

        for anime in sentences.anime_name.unique():
            st.markdown('## ' + anime)
            anime_sentences = sentences[sentences.anime_name == anime].drop_duplicates()
            for sent in anime_sentences.content.values:
                st.markdown(sent)

                translator = Translator()
                translation = translator.translate(sent).text
                st.markdown(translation)

                tts = gtts.gTTS(sent, lang='ja')
                tts.save('sent.mp3')
                st.audio('sent.mp3')

                st.markdown('<br>', unsafe_allow_html=True)