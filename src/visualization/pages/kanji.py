import streamlit as st
import re

from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.content_dependencies import ContentDependencies
from modules.models.study_order import StudyOrder
from src.utils import color_target_kanji, get_anime_info, get_audio, make_spoiler_html
from src.visualization.login import initialize_page

if initialize_page():
    user = st.session_state['session'].get_user()

    st.title('Estudos de Kanji')

    recommender = KanjiRecommendationManager(user)
    kanji_order = recommender.get_latest_model()

    kanji = st.selectbox(
        'Selecione o Kanji que você gostaria de estudar',
        options=kanji_order.Kanji.values
    )
    kanji_data = kanji_order[kanji_order.Kanji == kanji].fillna('')
    
    examples = kanji_data['Examples'].values[0]
    examples_list = [
            [re.sub('"', '', i).strip() for i in example.split('", "')] for example in
            re.split('\[|\],?\s?', examples[1:-1])
            if example.strip() != ''
        ]
    
    known_kanji = st.session_state['anki_manager'].get_unlocked_kanji()
    unlocked_kanji = kanji_order[
        (kanji_order.Kanji.isin(
            known_kanji
        )) |
        (kanji_order.Kanji == kanji)
    ]

    dependencies = ContentDependencies(user.get_unified_subtitles())
    study = StudyOrder(
        dependencies=dependencies,
        unlocked_kanji=unlocked_kanji,
        kanji_order=kanji_order
    )
    all_sentences = study.get_unlocked_sentences()
    sentences = all_sentences[
        all_sentences.content.apply(
            lambda a: kanji in a
        )
    ]
    kanji_name = kanji_order[kanji_order.Kanji == kanji]['Name'].values[-1]
    filename = 'https://media.kanjialive.com/kanji_animations/kanji_mp4/' + kanji_name + '_00.mp4'

    c1, c2, c3 = st.columns((1, 1, 3))

    with c1:
        st.markdown(
            '<h1 style="font-size:150px;">' + kanji + '</h1>',
            unsafe_allow_html=True
        )
        st.video(filename)
        st.markdown(
            '- ' + kanji_data['Kunyomi'].values[0].capitalize() + ', ' +\
            kanji_data['Onyomi'].values[0].capitalize() + '\n' +\
            '- ' + kanji_data['Meaning'].values[0].capitalize()
        )

        if kanji in known_kanji:
            st.success('Kanji conhecido')

    with c2:
        st.markdown('## Palavras')
        for example in examples_list:
            meaning = ''
            if len(example) > 1:
                meaning = ' <p style="color:lightgray;">' +\
                    example[1].capitalize() +\
                '</p></ul>'
            st.markdown(
                '<ul> ' + example[0] + meaning,
                unsafe_allow_html=True
            )

    with c3:
        st.markdown('## Frases')
        if len(sentences) == 0:
            st.warning('Nenhuma frase para estes Kanji! Tente estudar mais um, ou adicionar mais animes.')
        else:
            anime = st.selectbox(
                'Escolha o anime',
                options=list(
                    sentences.anime_name.unique()
                )
            )
            maximo = st.selectbox(
                'Escolha o máximo de frases',
                options=[10, 50, 100, len(sentences)]
            )

            sentences = sentences[
                sentences.anime_name == anime
            ].drop_duplicates(
                subset=['anime_name', 'content']
            )[:maximo]

            for _, row in sentences.iterrows():
                sent = row.content

                st.markdown(
                    get_anime_info(
                        row.anime_name,
                        row.filename,
                        row.start_time
                    )
                )

                st.markdown(
                    color_target_kanji(sent, kanji),
                    unsafe_allow_html=True
                )

                get_audio(sent)
                st.audio('sent.mp3')
            
                st.markdown(
                    make_spoiler_html(sent),
                    unsafe_allow_html=True
                )

                st.markdown('<br>', unsafe_allow_html=True)