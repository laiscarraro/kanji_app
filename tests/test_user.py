from src.visualization import user
import pytest
import pandas as pd

# Fixtures

@pytest.fixture
def laiscarraro():
    user_information = pd.DataFrame(
        [(1, 'laiscarraro', 'Laís')],
        columns=['user_id', 'user_login', 'user_name']
    )
    animes = ['a', 'b']
    return user.User(user_information, animes)


# Tests

def test_get_id(laiscarraro):
    laiscarraro_id = laiscarraro.get_id()
    assert laiscarraro_id == 1

def test_get_name(laiscarraro):
    laiscarraro_name = laiscarraro.get_name()
    assert laiscarraro_name == 'Laís'

def test_get_login(laiscarraro):
    laiscarraro_login = laiscarraro.get_login()
    assert laiscarraro_login == 'laiscarraro'

def test_get_animes(laiscarraro):
    laiscarraro_animes = laiscarraro.get_animes()
    assert (
        laiscarraro_animes[0] == 'a' and
        laiscarraro_animes[1] == 'b'
    )
