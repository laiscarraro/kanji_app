from modules.builders import user_builder
from modules.managers import anime_manager
import pytest
import pandas as pd

# Fixtures

@pytest.fixture
def test_user():
    return user_builder.UserBuilder.get_user().from_login('test_user').build()

@pytest.fixture
def test_user_no_animes():
    return user_builder.UserBuilder.get_user().from_login('test_user_no_animes').build()

@pytest.fixture
def user_animes(test_user):
    animes = pd.read_parquet('data/user_anime.parquet')
    return animes[animes.user_id == test_user.id]

@pytest.fixture
def test_anime_manager(test_user):
    return anime_manager.AnimeManager(test_user)

@pytest.fixture
def test_anime_manager_no_animes(test_user_no_animes):
    return anime_manager.AnimeManager(test_user_no_animes)


# Tests

def test_get_available_animes(test_anime_manager):
    available = test_anime_manager.get_available_animes()
    assert (
        1619 not in available.anime_id.values and
        2031 in available.anime_id.values
    )

def test_new_anime(test_anime_manager):
    new = test_anime_manager.new_anime(2031)
    assert new.id == 2031

def test_add_anime_to_user(test_anime_manager):
    has_before = test_anime_manager.user.has_anime(2031)
    test_anime_manager.add_anime_to_user(2031)
    has_after = test_anime_manager.user.has_anime(2031)
    assert not has_before and has_after

    test_anime_manager.remove_anime_from_user(2031)

def test_add_anime_to_dataframe(test_anime_manager, user_animes, test_user):
    has_before = 2031 in user_animes.anime_id.values
    test_anime_manager.add_anime_to_dataframe(2031)

    user_animes_after = pd.read_parquet('data/user_anime.parquet')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = 2031 in user_animes.anime_id.values
    assert not has_before and has_after

    test_anime_manager.remove_anime_from_dataframe(2031)

def test_add_anime(test_anime_manager, user_animes, test_user):
    has_before = (
        test_anime_manager.user.has_anime(2031) and
        2031 in user_animes.anime_id.values
    )
    added = test_anime_manager.add_anime(2031)
    user_animes_after = pd.read_parquet('data/user_anime.parquet')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = (
        test_anime_manager.user.has_anime(2031) and
        2031 in user_animes.anime_id.values
    )
    assert not has_before and added and has_after

    test_anime_manager.remove_anime_from_dataframe(2031)
    test_anime_manager.remove_anime_from_user(2031)

def test_add_anime_user_with_no_anime(test_anime_manager_no_animes, user_animes, test_user_no_animes):
    has_before = (
        test_anime_manager_no_animes.user.has_anime(2031) and
        2031 in user_animes.anime_id.values
    )
    added = test_anime_manager_no_animes.add_anime(2031)
    user_animes_after = pd.read_parquet('data/user_anime.parquet')
    user_animes = user_animes_after[user_animes_after.user_id == test_user_no_animes.id]
    has_after = (
        test_anime_manager_no_animes.user.has_anime(2031) and
        2031 in user_animes.anime_id.values
    )
    assert not has_before and added and has_after

    test_anime_manager_no_animes.remove_anime_from_dataframe(2031)
    test_anime_manager_no_animes.remove_anime_from_user(2031)

def test_remove_anime_from_user(test_anime_manager):
    has_before = test_anime_manager.user.has_anime(62)
    test_anime_manager.remove_anime_from_user(62)
    has_after = test_anime_manager.user.has_anime(62)
    assert has_before and not has_after

    test_anime_manager.add_anime_to_user(62)

def test_remove_anime_from_dataframe(test_anime_manager, user_animes, test_user):
    has_before = 62 in user_animes.anime_id.values
    user_animes_before = pd.read_parquet('data/user_anime.parquet').copy()
    test_anime_manager.remove_anime_from_dataframe(62)

    user_animes_after = pd.read_parquet('data/user_anime.parquet')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = 62 in user_animes.anime_id.values
    assert has_before and not has_after

    user_animes_before.to_parquet('data/user_anime.parquet', index=False)

def test_remove_anime(test_anime_manager, user_animes, test_user):
    has_before = (
        test_anime_manager.user.has_anime(62) and
        62 in user_animes.anime_id.values
    )
    user_animes_before = pd.read_parquet('data/user_anime.parquet').copy()
    removed = test_anime_manager.remove_anime(62)

    user_animes_after = pd.read_parquet('data/user_anime.parquet')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = (
        test_anime_manager.user.has_anime(62) and
        62 in user_animes.anime_id.values
    )
    assert has_before and removed and not has_after

    test_anime_manager.add_anime_to_user(62)
    user_animes_before.to_parquet('data/user_anime.parquet', index=False)