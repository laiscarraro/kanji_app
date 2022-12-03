from modules import anime
import pytest
import pandas as pd

# Fixtures

@pytest.fixture
def test_anime():
    subtitles = pd.DataFrame(
        [('test_anime',
        'test_anime001.srt',
        '1:00', '1:01', 'test')],
        columns=[
            'anime_name', 'filename',
            'start_time', 'end_time',
            'content'
        ]
    )

    return anime.Anime(
        id = 1,
        name = 'test_anime',
        subtitles = subtitles
    )


# Tests

def test_get_id(test_anime):
    test_anime_id = test_anime.get_id()
    assert test_anime_id == 1

def test_get_name(test_anime):
    test_anime_name = test_anime.get_name()
    assert test_anime_name == 'test_anime'

def test_get_subtitles(test_anime):
    test_anime_subtitles = test_anime.get_subtitles()
    assert test_anime_subtitles.content.values[0] == 'test'