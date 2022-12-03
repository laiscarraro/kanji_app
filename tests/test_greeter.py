from modules import greeter
from modules import user
from modules.builders import anime_builder
import pytest

# Fixtures

@pytest.fixture
def test_greeter():
    return greeter.Greeter()

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

def test_replace_name(test_greeter, test_user):
    greeting = 'Oi, NOME! Teste de greeting'
    assert (
        test_greeter.replace_name(greeting, test_user)
        == 'Oi, test_name! Teste de greeting'
    )

def test_greet(test_greeter, test_user):
    greeting = test_greeter.greet(test_user)
    assert (
        'NOME' not in greeting and
        'test_name' in greeting
    )