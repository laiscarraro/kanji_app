from modules.managers import kanji_recommendation_manager
from modules.builders import user_builder
import pytest

# Fixtures

@pytest.fixture
def test_user():
    user = user_builder.UserBuilder().get_user().from_login('test_user')
    return user.build()

@pytest.fixture
def test_manager(test_user):
    return kanji_recommendation_manager.KanjiRecommendationManager(test_user)


# Tests

def test_get_animes_from_ids(test_manager):
    anime_ids = [1619]
    animes = test_manager.get_animes_from_ids(anime_ids)
    assert (
        len(animes) == len(anime_ids) and
        animes[0].get_name() == 'shigatsu wa kimi no uso'
    )

def test_search_latest_model(test_manager):
    latest = test_manager.search_latest_model()
    assert (
        len(latest) > 0 and
        latest.filename.values[0] == 'test'
    )

def test_update_latest_model_metadata(test_manager):
    before_user_configuration = test_manager.user_configuration.copy()
    test_manager.update_latest_model_metadata('test2')
    assert (
        test_manager.search_latest_model().filename.values[0] == 'test2'
    )
    before_user_configuration.to_csv('data/models/user_configuration.csv', sep=';', index=None)

def test_handle_model_filename(test_manager):
    anime_ids = [62]
    features = ['Strokes', 'Grade']
    existing_filename = test_manager.handle_model_filename(anime_ids, features)
    
    assert existing_filename == 'test'

def test_make_default_model(test_manager):
    metadata_before = test_manager.handler.metadata.copy()
    before_user_configuration = test_manager.user_configuration.copy()

    test_manager.make_default_model()
    default_filename = test_manager.search_latest_model()

    assert (
        len(default_filename) == 1 and
        default_filename.filename.values[0] != 'test'
    )

    before_user_configuration.to_csv('data/models/user_configuration.csv', sep=';', index=None)
    metadata_before.to_csv('data/models/metadata.csv', sep=';', index=None)

def test_get_latest_model_filename(test_manager):
    filename = test_manager.get_latest_model_filename()
    assert filename == 'test'

def test_update_latest_model(test_manager):
    pass

def test_get_kanji_information(test_manager):
    pass

def test_get_latest_model(test_manager):
    pass