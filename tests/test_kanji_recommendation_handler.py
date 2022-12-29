from modules.handlers import kanji_recommendation_handler
from modules.builders import anime_builder
import pandas as pd
import os
import pytest

# Fixtures

@pytest.fixture
def test_handler():
    h = kanji_recommendation_handler.KanjiRecommendationHandler()
    subs = pd.read_parquet('data/subtitles.parquet')
    h.set_subtitles(
        subs[subs.anime_name.isin(
            ['shigatsu wa kimi no uso', 'yuri!!! on ice']
        )]
    )
    return h


# Tests

def test_get_possible_features(test_handler):
    possible_features = test_handler.get_possible_features()
    assert (
        len(possible_features) > 0 and
        possible_features[0] == 'Strokes'
    )

def test_set_features(test_handler):
    before = test_handler.features
    test_handler.set_features(
        ['Strokes', 'Grade']
    )
    after = test_handler.features

    assert (
        len(before) > len(after)
        and len(after) == 2
        and after[0] == 'Strokes'
        and after[1] == 'Grade'
    )

def test_set_anime_list(test_handler):
    before = test_handler.anime_list
    test_handler.set_anime_list([2031, 1619])
    after = test_handler.anime_list

    assert (
        len(before) == 0 and
        len(before) < len(after)
        and len(after) == 2
        and after[0] == 2031
    )

def test_search_trained_model_filename(test_handler):
    model_not_exists = {
        'animes': [
            anime_builder.AnimeBuilder().get_anime().from_id(2031).build(),
            anime_builder.AnimeBuilder().get_anime().from_id(1619).build()
        ],
        'features': ['f1']
    }

    test_handler.set_anime_list(model_not_exists['animes'])
    test_handler.set_features(model_not_exists['features'])
    second = test_handler.search_trained_model_filename()

    assert second is None

def test_update_metadata(test_handler):
    metadata_before = test_handler.metadata.copy()
    test_handler.update_metadata('test2')
    metadata_after = test_handler.metadata

    assert (
        len(metadata_before) < len(metadata_after)
        and 'test2' in metadata_after.filename.values
    )

    metadata_before.to_parquet('data/models/metadata.parquet', index=False)

def test_save_model(test_handler):
    metadata_before = test_handler.metadata.copy()
    model = pd.DataFrame(None)
    filename = test_handler.save_model(model)

    assert (
        filename not in metadata_before.filename.values and
        filename in test_handler.metadata.filename.values and
        filename in os.listdir('data/models')
    )

    os.remove('data/models/'+filename)
    metadata_before.to_parquet('data/models/metadata.parquet', index=False)


def test_train_model(test_handler):
    metadata_before = test_handler.metadata.copy()
    model = {
        'animes': [
            anime_builder.AnimeBuilder().get_anime().from_id(2031).build(),
            anime_builder.AnimeBuilder().get_anime().from_id(1619).build()
        ],
        'features': ['Strokes', 'Grade']
    }
    test_handler.set_anime_list(model['animes'])
    test_handler.set_features(model['features'])
    filename = test_handler.train_model()

    assert (
        filename not in metadata_before.filename.values and
        filename in test_handler.metadata.filename.values and
        filename in os.listdir('data/models')
    )

    os.remove('data/models/'+filename)
    metadata_before.to_parquet('data/models/metadata.parquet', index=False)


def test_get_model_filename(test_handler):
    metadata_before = test_handler.metadata.copy()
    model1 = {
        'animes': [
            anime_builder.AnimeBuilder().get_anime().from_id(2031).build(),
            anime_builder.AnimeBuilder().get_anime().from_id(1619).build()
        ],
        'features': ['Strokes', 'Grade']
    }
    test_handler.set_anime_list(model1['animes'])
    test_handler.set_features(model1['features'])
    filename1 = test_handler.get_model_filename()

    model2 = {
        'animes': [
            anime_builder.AnimeBuilder().get_anime().from_id(1619).build()
        ],
        'features': ['Strokes', 'Grade']
    }
    test_handler.set_anime_list(model2['animes'])
    test_handler.set_features(model2['features'])
    filename2 = test_handler.get_model_filename()

    assert (
        filename2 is not None and filename1 is not None
        and len(filename1) > len('kanji_model_')
    )
    try:
        os.remove('data/models/'+filename1)
        os.remove('data/models/'+filename2)
    except:
        pass
    metadata_before.to_parquet('data/models/metadata.parquet', index=False)
