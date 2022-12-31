import streamlit as st
import pandas as pd

from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.content_dependencies import ContentDependencies
from modules.models.study_order import StudyOrder
from src.utils import color_target_kanji, get_audio, make_spoiler_html, get_anime_info, get_player_link
from src.visualization.login import initialize_page

if initialize_page():
    user = st.session_state['session'].get_user()

    st.title('Leitura profunda')

    known_words = pd.DataFrame(
        st.session_state['anki_manager'].get_unlocked_words(),
        columns=['Word']
    )
    known_words['index'] = known_words.index
    known_words['index'] = known_words['index'].apply(str)
    dependencies = ContentDependencies(user.get_unified_subtitles())
    study = StudyOrder(
        dependencies=dependencies,
        unlocked_words=known_words,
        anki_words=st.session_state['anki_manager'].get_words()
    )
    sequences = study.get_unlocked_sequences(type='words')

    for _, row in sequences.sample(10).iterrows():
        sent = row.content

        st.markdown(
            get_anime_info(
                row.anime_name,
                row.filename,
                row.start_time
            )
        )

        st.markdown(
            color_target_kanji(sent, 'a'),
            unsafe_allow_html=True
        )

        get_audio(sent)
        st.audio('sent.mp3')
    
        st.markdown(
            make_spoiler_html(sent),
            unsafe_allow_html=True
        )
        
        get_player_link(
            row.anime_name,
            row.filename,
            row.content,
            row.start_time
        )

        st.markdown('<br>', unsafe_allow_html=True)