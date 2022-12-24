from modules import user
from modules.builders import anime_builder
from modules.builders import user_builder
from modules.anime import Anime
import pytest

# Fixtures

@pytest.fixture
def test_user():
    login = 'test_user'
    name = 'Teste-1'
    id = -1
    anime_ids = [1619, 62]

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
def laiscarraro():
    l = user_builder.UserBuilder(
    ).get_user().from_login('laiscarraro').build()
    return l



# Tests

def test_get_id(test_user):
    test_user_id = test_user.get_id()
    assert test_user_id == -1

def test_get_name(test_user):
    test_user_name = test_user.get_name()
    assert test_user_name == 'Teste-1'

def test_get_login(test_user):
    test_user_login = test_user.get_login()
    assert test_user_login == 'test_user'

def test_get_animes(test_user):
    test_user_animes = test_user.get_animes()
    assert (
        test_user_animes[1].id == 62 and
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
        and animes_df.id.values[0] == 1619
    )

def test_has_anime(test_user):
    assert (
        test_user.has_anime(1619) and
        not test_user.has_anime(100000000000)
    )

def test_get_unified_subtitles(laiscarraro):
    subs = laiscarraro.get_unified_subtitles()
    print(subs)
    assert subs is None