from modules.models import word_order
import os
import pandas as pd
import pytest

# Fixtures

@pytest.fixture
def orderer():
    kanji_order = pd.read_parquet('data/models/'+[
        f for f in os.listdir('data/models/')
        if 'kanji_order' in f
    ][0])
    subtitles = pd.read_csv('data/subtitles.csv', sep=';')
    subtitles = subtitles[subtitles.anime_name == 'ousama ranking']
    return word_order.WordOrder(kanji_order, subtitles)


# Tests

def test_tokenize(orderer):
    sentence = '私の名前わライスです。'
    tokenized = [
        '私', 'の', '名前', 'わ', 'ライス', 'です', '。'
    ]
    assert orderer.tokenize(sentence) == tokenized

def test_get_word_df(orderer):
    word_df = orderer.get_word_df()
    assert (
        len(word_df.dropna()) > 0 and
        '私' in word_df.word.values
    )

def test_make_bag_of_kanji(orderer):
    vec, bow = orderer.make_bag_of_kanji()
    assert (
        bow.shape[0] > 0 and
        len(vec.get_feature_names_out()) > 0 and
        '私' in vec.get_feature_names_out()
    )

def test_get_kanji_df(orderer):
    kanji_list = [
        '私', 'の', '名', '前', 'わ', 'ラ', 'イ', 'ス', 'で', 'す', '。'
    ]
    kanji_df = orderer.get_kanji_df(kanji_list)
    print(kanji_df.head())
    assert (
        len(kanji_df.dropna()) > 0 and
        '私' in kanji_df.Kanji.values
    )

def test_get_score_matrix(orderer):
    vec, bow = orderer.make_bag_of_kanji()
    score_matrix = orderer.get_score_matrix()
    assert score_matrix.shape[0] == bow.shape[0]

def test_make_word_scores(orderer):
    orderer.make_word_scores()
    assert (
        len(orderer.word_scores.dropna()) > 0 and
         len(orderer.word_scores[
            orderer.word_scores.score <= 0
         ]) == 0
    )

def test_get_words_with_kanji(orderer):
    orderer.make_word_scores()
    kanji = '私'
    words_with_kanji = orderer.get_words_with_kanji(kanji)
    assert (
        len(words_with_kanji.dropna())
        == 
        len(words_with_kanji[
            words_with_kanji.word.apply(
                lambda w: kanji in w
            )
        ])
    )

def test_get_reference_words(orderer):
    top = orderer.get_reference_words()
    print(top)
    assert False