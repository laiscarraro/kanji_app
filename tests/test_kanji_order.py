from modules.models import kanji_order
from modules.builders import user_builder
import pandas as pd
import pytest

# Fixtures

@pytest.fixture
def kanji_model():
    user = user_builder.UserBuilder.get_user().from_login('test_user').build()
    kanji_model = kanji_order.KanjiOrder(user.get_animes(), ['Strokes', 'Grade'])
    return kanji_model


# Tests

def test_make_unified_subtitles(kanji_model):
    kanji_model.make_unified_subtitles()
    assert (
        isinstance(
            kanji_model.unified_subtitles,
            pd.DataFrame
        )
    )

def test_make_kanji_frequency_in_animes(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    assert (
        len(kanji_model.kanji_frequency_in_animes.dropna()) > 0
        and kanji_model.kanji_frequency_in_animes[
            'Frequency in animes'
        ].values[0] > 0
    )

def test_make_kanji_data(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    assert (
        'Frequency in animes' in kanji_model.kanji_data.columns
        and 'Strokes' in kanji_model.kanji_data.columns
    )

def test_split_dataset(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    kanji_model.split_dataset()
    assert (
        kanji_model.x_train is not None and
        len(kanji_model.x_train.dropna()) > 0
    )

def test_train(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    kanji_model.split_dataset()
    kanji_model.train()
    assert (
        kanji_model.pipeline['Scaler'] is not None and
        kanji_model.pipeline['ElasticNet'] is not None
    )

def test_make_coeficients(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    kanji_model.split_dataset()
    kanji_model.train()
    kanji_model.make_coeficients()
    assert (
        kanji_model.coeficients is not None and
        len(kanji_model.coeficients) > 0
    )

def test_make_new_features(kanji_model):
    kanji_model.make_new_features()
    assert 'Frequency in animes' in kanji_model.new_features

def test_transform_model_to_anime(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    kanji_model.split_dataset()
    kanji_model.train()
    kanji_model.make_coeficients()
    kanji_model.make_new_features()
    kanji_model.transform_model_to_anime()
    assert (
        len(kanji_model.anime_model.dropna()) > 0 and
        'Frequency in animes' in kanji_model.anime_model.columns
    )

def test_replace_frequency_to_anime(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    kanji_model.split_dataset()
    kanji_model.train()
    kanji_model.make_coeficients()
    kanji_model.make_new_features()
    kanji_model.transform_model_to_anime()
    kanji_model.replace_frequency_to_anime()
    print(kanji_model.anime_model.head())
    assert (
        len(
            kanji_model.anime_model['Frequency in animes'].dropna()
         ) == len(kanji_model.anime_model)
    )

def test_make_suggested_order(kanji_model):
    kanji_model.make_unified_subtitles()
    kanji_model.make_kanji_frequency_in_animes()
    kanji_model.make_kanji_data()
    kanji_model.split_dataset()
    kanji_model.train()
    kanji_model.make_coeficients()
    kanji_model.make_new_features()
    kanji_model.transform_model_to_anime()
    kanji_model.replace_frequency_to_anime()
    kanji_model.make_suggested_order()
    assert (
        kanji_model.suggested_order is not None and
        len(kanji_model.suggested_order) == len(kanji_model.anime_model)
    )

def test_get_kanji_order(kanji_model):
    order = kanji_model.get_kanji_order()
    assert (
        order['Suggested Order'] is not None and
        len(order.dropna()) == len(kanji_model.anime_model)
    )