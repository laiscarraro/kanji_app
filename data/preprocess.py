import pandas as pd
from data import fetch as fecth
from collections import Counter

kanji_database = pd.merge(fecth.kanji_metadata, fecth.heisig_order, on='Kanji')

grade_order = pd.DataFrame(kanji_database.sort_values(by='Grade').sort_values(by='Strokes')['Kanji'])
grade_order['grade_order'] = list(range(1, len(kanji_database)+1))

strokes_order = pd.DataFrame(kanji_database.sort_values(by='Strokes')['Kanji'])
strokes_order['strokes_order'] = list(range(1, len(kanji_database)+1))

freq_order = pd.DataFrame(kanji_database.sort_values(by='Kanji Frequency without Proper Nouns')['Kanji'])
freq_order['freq_order'] = list(range(1, len(kanji_database)+1))

kanji_order = pd.merge(pd.merge(pd.merge(grade_order, strokes_order, on='Kanji'), freq_order, on='Kanji'), fecth.heisig_order, on='Kanji')

# Data processing functions

def top_kanji_freq(subs, n=0):
    kanji = ''
    for s in subs:
        for i in s:
            if i in list(kanji_database['Kanji']):
                kanji += i
    
    if n == 0: n = len(kanji)
    return Counter(kanji).most_common(n)