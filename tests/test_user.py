from modules import user
from modules.builders import anime_builder
from modules.anime import Anime
import pytest

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


# Tests

def test_get_id(test_user):
    test_user_id = test_user.get_id()
    assert test_user_id == 1

def test_get_name(test_user):
    test_user_name = test_user.get_name()
    assert test_user_name == 'test_name'

def test_get_login(test_user):
    test_user_login = test_user.get_login()
    assert test_user_login == 'test_login'

def test_get_animes(test_user):
    test_user_animes = test_user.get_animes()
    assert (
        test_user_animes[1].id == 2 and
        isinstance(test_user_animes[1], Anime)
    )

def test_set_animes(test_user):
    animes_before = test_user.get_animes()
    test_user.set_animes(None)
    animes_after = test_user.get_animes()
    assert (
        animes_before is not None and
        animes_after is None
    )

def test_count_animes(test_user):
    assert test_user.count_animes() == 2

def test_get_animes_df(test_user):
    animes_df = test_user.get_animes_df()
    assert (
        len(animes_df) == 2
        and animes_df.id.values[0] == 1
    )

def test_has_anime(test_user):
    assert (
        test_user.has_anime(1) and
        not test_user.has_anime(1000000)
    )