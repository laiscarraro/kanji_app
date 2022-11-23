from src.visualization import anime
import pytest
import pandas as pd

# Fixtures

@pytest.fixture
def shigatsu():
    anime_information = pd.DataFrame(
        [(1, 'shigatsu')],
        columns=['anime_id', 'anime_name']
    )
    return anime.Anime(anime_information)


# Tests

def test_get_id(shigatsu):
    shigatsu_id = shigatsu.get_id()
    assert shigatsu_id == 1

def test_get_name(shigatsu):
    shigatsu_name = shigatsu.get_name()
    assert shigatsu_name == 'shigatsu'