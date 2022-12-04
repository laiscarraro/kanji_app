from modules import user
from modules.builders import anime_builder
from modules import anime_manager
import pytest
import pandas as pd

# Fixtures

@pytest.fixture
def test_user():
    login = 'test_login'
    name = 'test_name'
    id = 1
    anime_ids = [1, 2]

    anime_list = [
        anime_builder.AnimeBuilder.get_anime().from_id(
            anime_id
        ).build() for anime_id in anime_ids
    ]
    return user.User(
        login=login,
        name=name,
        id=id,
        animes=anime_list
    )

@pytest.fixture
def test_user_no_animes():
    login = 'test_login_no_animes'
    name = 'test_name_no_animes'
    id = 10000000
    anime_list = []

    return user.User(
        login=login,
        name=name,
        id=id,
        animes=anime_list
    )

@pytest.fixture
def user_animes(test_user):
    animes = pd.read_csv('data/user_anime.csv', sep=';')
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
        1 not in available.anime_id.values and
        3 in available.anime_id.values
    )

def test_new_anime(test_anime_manager):
    new = test_anime_manager.new_anime(3)
    assert new.id == 3

def test_add_anime_to_user(test_anime_manager):
    has_before = test_anime_manager.user.has_anime(3)
    test_anime_manager.add_anime_to_user(3)
    has_after = test_anime_manager.user.has_anime(3)
    assert not has_before and has_after

    test_anime_manager.remove_anime(3)

def test_add_anime_to_dataframe(test_anime_manager, user_animes, test_user):
    has_before = 3 in user_animes.anime_id.values
    test_anime_manager.add_anime_to_dataframe(3)

    user_animes_after = pd.read_csv('data/user_anime.csv', sep=';')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = 3 in user_animes.anime_id.values
    assert not has_before and has_after

    test_anime_manager.remove_anime(3)

def test_add_anime(test_anime_manager, user_animes, test_user):
    has_before = (
        test_anime_manager.user.has_anime(3) and
        3 in user_animes.anime_id.values
    )
    added = test_anime_manager.add_anime(3)
    user_animes_after = pd.read_csv('data/user_anime.csv', sep=';')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = (
        test_anime_manager.user.has_anime(3) and
        3 in user_animes.anime_id.values
    )
    assert not has_before and added and has_after

    test_anime_manager.remove_anime(3)

def test_add_anime_user_with_no_anime(test_anime_manager_no_animes, user_animes, test_user_no_animes):
    has_before = (
        test_anime_manager_no_animes.user.has_anime(3) and
        3 in user_animes.anime_id.values
    )
    added = test_anime_manager_no_animes.add_anime(3)
    user_animes_after = pd.read_csv('data/user_anime.csv', sep=';')
    user_animes = user_animes_after[user_animes_after.user_id == test_user_no_animes.id]
    has_after = (
        test_anime_manager_no_animes.user.has_anime(3) and
        3 in user_animes.anime_id.values
    )
    assert not has_before and added and has_after

    test_anime_manager_no_animes.remove_anime(3)

def test_remove_anime_from_user(test_anime_manager):
    has_before = test_anime_manager.user.has_anime(2)
    test_anime_manager.remove_anime_from_user(2)
    has_after = test_anime_manager.user.has_anime(2)
    assert has_before and not has_after

    test_anime_manager.add_anime_to_user(2)

def test_remove_anime_from_dataframe(test_anime_manager, user_animes, test_user):
    has_before = 2 in user_animes.anime_id.values
    test_anime_manager.remove_anime_from_dataframe(2)

    user_animes_after = pd.read_csv('data/user_anime.csv', sep=';')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = 2 in user_animes.anime_id.values
    assert has_before and not has_after

    test_anime_manager.user_animes.to_csv('data/user_anime.csv', sep=';', index=None)

def test_remove_anime(test_anime_manager, user_animes, test_user):
    has_before = (
        test_anime_manager.user.has_anime(2) and
        2 in user_animes.anime_id.values
    )
    removed = test_anime_manager.remove_anime(2)
    user_animes_after = pd.read_csv('data/user_anime.csv', sep=';')
    user_animes = user_animes_after[user_animes_after.user_id == test_user.id]
    has_after = (
        test_anime_manager.user.has_anime(2) and
        2 in user_animes.anime_id.values
    )
    assert has_before and removed and not has_after

    test_anime_manager.user_animes.to_csv('data/user_anime.csv', sep=';', index=None)
    test_anime_manager.add_anime_to_user(2)