import streamlit as st

from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.content_dependencies import ContentDependencies
from modules.models.study_order import StudyOrder
from src.utils import color_target_kanji, get_audio, make_spoiler_html, get_anime_info, get_player_link

if 'user_found' in st.session_state and st.session_state['user_found']:
    user = st.session_state['session'].get_user()

    st.title('Leitura')

    recommender = KanjiRecommendationManager(user)
    kanji_order = recommender.get_latest_model()

    unlocked_kanji = kanji_order[
        (kanji_order.Kanji.isin(
            [k for k in user.get_kanji()]
        ))
    ]

    dependencies = ContentDependencies(user.get_unified_subtitles())
    study = StudyOrder(unlocked_kanji, dependencies, kanji_order)
    sequences = study.get_unlocked_sequences()

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
else:
    st.error('Usuário não encontrado.')