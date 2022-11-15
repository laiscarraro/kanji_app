import streamlit as st
from src.page_files import kanji_recommend
from src.page_files import writing
from src.page_files import vocabulary

st.set_page_config(layout="wide")

# Tirar isso daqui
def top_kanji_freq(self, subtitles, n=0):
    kanji = ''
    for s in subtitles:
        for i in s:
            if i in list(self.kanji_database[self.key]):
                kanji += i
    
    if n == 0: n = len(kanji)
    return Counter(kanji).most_common(n)


tabs = st.tabs(['Kanji', 'Escrita', 'Vocabulário'])

with tabs[0]:
    kanji_recommend.render_page()
with tabs[1]:
    writing.render_page()
with tabs[2]:
    vocabulary.render_page()