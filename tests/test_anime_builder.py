from modules.builders import anime_builder
from modules.anime import Anime
import pytest

# Fixtures

@pytest.fixture
def test_anime_builder():
    return anime_builder.AnimeBuilder.get_anime()


# Tests

def test_get_anime(test_anime_builder):
    original_anime_builder = test_anime_builder.get_anime()
    other_anime_builder = anime_builder.AnimeBuilder.get_anime()
    assert id(original_anime_builder) != id(other_anime_builder)

def test_from_id(test_anime_builder):
    id_before = test_anime_builder.id
    test_anime_builder.from_id(1)
    id_after = test_anime_builder.id
    assert (
        id_before is None
        and id_after == 1
    )

def test_get_anime_information(test_anime_builder):
    info = test_anime_builder.from_id(1).get_anime_information()
    assert info.anime_id.values[0] == 1

def test_set_name(test_anime_builder):
    info = test_anime_builder.from_id(1).get_anime_information()
    test_anime_builder.set_name()
    assert test_anime_builder.name == info.anime_name.values[0]

def test_set_subtitles(test_anime_builder):
    test_anime_builder.from_id(1)
    subtitles_before = test_anime_builder.subtitles
    test_anime_builder.set_name()
    test_anime_builder.set_subtitles()
    subtitles_after = test_anime_builder.subtitles
    assert (
        subtitles_before is None and
        subtitles_after is not None and
        subtitles_after.anime_name.values[0] == test_anime_builder.name
    )

def test_build(test_anime_builder):
    anime = test_anime_builder.from_id(1).build()
    assert (
        isinstance(anime, Anime) and
        anime.get_id() == 1
    )
    