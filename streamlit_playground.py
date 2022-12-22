import streamlit as st

from modules import session
from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.content_dependencies import ContentDependencies
from modules.models.study_order import StudyOrder

import gtts
import fugashi
from googletrans import Translator
import re
import pykakasi

st.set_page_config(layout="wide")

session = session.Session()
session.set_user('laiscarraro')
user = session.get_user()

st.title('Estudos de Kanji')

recommender = KanjiRecommendationManager(user)
kanji_order = recommender.get_latest_model()

kanji = st.selectbox(
    'Selecione o Kanji que você gostaria de estudar',
    options=kanji_order.Kanji.values
)
audio = st.checkbox('Mostrar áudio', value=True)
translation = st.checkbox('Mostrar tradução', value=True)

kanji_data = kanji_order[kanji_order.Kanji == kanji].fillna('')

examples = kanji_data['Examples'].values[0]
examples_list = [
        [re.sub('"', '', i).strip() for i in example.split('", "')] for example in
        re.split('\[|\],?\s?', examples[1:-1])
        if example.strip() != ''
    ]

n_unlocked_kanji = kanji_data['Suggested Order'].values[0]
unlocked_kanji = kanji_order.iloc[:n_unlocked_kanji]
dependencies = ContentDependencies(user.get_unified_subtitles())
study = StudyOrder(unlocked_kanji, dependencies, kanji_order)
all_sentences = study.get_unlocked_sentences()
sentences = all_sentences[
    all_sentences.content.apply(
        lambda a: kanji in a
    )
]

def kanji_html(sent):
    tagger = fugashi.Tagger()
    kks = pykakasi.kakasi()
    words = [word.surface for word in tagger(sent)]
    md = ''
    for w in words:
        printed = False
        target = kanji in w
        if target:
            md += '<span style="color:lightgreen;">'
        else:
            md += '<span>'
        for k in w:
            if k in kanji_order.Kanji.str.cat(sep=''):
                furigana = ''.join([f['hira'] for f in kks.convert(w)])
                md += '<ruby><rb>' + w + '</rb><rt>' + furigana + '</rt></ruby>'
                printed = True
                break
        if not printed:
            md += w
            
        md += '</span> '

    return md

kanji_name = kanji_order[kanji_order.Kanji == kanji]['Name'].values[-1]
filename = 'https://media.kanjialive.com/kanji_animations/kanji_mp4/' + kanji_name + '_00.mp4'

c1, c2, c3 = st.columns((1, 1, 3))

with c1:
    st.video(filename)
    st.markdown(
        '- ' + kanji_data['Kunyomi'].values[0].capitalize() + ', ' +\
        kanji_data['Onyomi'].values[0].capitalize() + '\n' +\
        '- ' + kanji_data['Meaning'].values[0].capitalize()
    )

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
    for _, row in sentences.iterrows():
        sent = row.content

        translator = Translator()
        translation = translator.translate(sent).text

        tagger = fugashi.Tagger()
        words = [word.surface for word in tagger(sent)]
        
        st.markdown(' ***' + row.anime_name + '***')
        # md = ''
        # for w in words:
        #     if kanji in w:
        #         md += '<span style="color:lightgreen;">' + kanji_html(w) + '</span> '
        #     else:
        #         md += kanji_html(w) + ' '
        # st.markdown(
        #     md, unsafe_allow_html=True
        # )
        st.markdown(
            kanji_html(sent), unsafe_allow_html=True
        )
        
        if translation:
            st.markdown(
                '<p style="color:lightgray;">' + translation + '</p></ul>',
                unsafe_allow_html=True
            )

        if audio:
            tts = gtts.gTTS(sent, lang='ja')
            tts.save('sent.mp3')
            st.audio('sent.mp3')

        st.markdown('<br>', unsafe_allow_html=True)