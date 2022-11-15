import streamlit as st
from page_files import kanji_recommend
from page_files import writing
from page_files import vocabulary

st.set_page_config(layout="wide")


tabs = st.tabs(['Kanji', 'Escrita', 'Vocabulário'])

with tabs[0]:
    kanji_recommend.render_page()
with tabs[1]:
    writing.render_page()
with tabs[2]:
    vocabulary.render_page()