from modules.builders import user_builder
from modules.user import User
import pytest

# Fixtures

@pytest.fixture
def test_user_builder():
    return user_builder.UserBuilder.get_user()


# Tests

def test_get_user(test_user_builder):
    original_user_builder = test_user_builder.get_user()
    other_user_builder = user_builder.UserBuilder.get_user()
    assert id(original_user_builder) != id(other_user_builder)

def test_from_login(test_user_builder):
    login_before = test_user_builder.login
    test_user_builder.from_login('laiscarraro')
    login_after = test_user_builder.login
    assert (
        login_before is None
        and login_after == 'laiscarraro'
    )

def test_set_user_information(test_user_builder):
    test_user_builder.from_login('laiscarraro').set_user_information()
    assert test_user_builder.user_information.user_login.values[0] == 'laiscarraro'

def test_user_found(test_user_builder):
    test_user_builder.from_login('laiscarraro').set_user_information()
    assert test_user_builder.user_found()

def test_user_not_found(test_user_builder):
    test_user_builder.from_login('banana').set_user_information()
    assert not test_user_builder.user_found()

def test_set_id(test_user_builder):
    test_user_builder.from_login('laiscarraro').set_user_information()
    test_user_builder.set_id()
    assert test_user_builder.id == test_user_builder.user_information.user_id.values[0]

def test_get_anime_ids(test_user_builder):
    user = test_user_builder.from_login('laiscarraro')
    user.set_user_information()
    test_user_builder.set_id()
    anime_ids = user.get_anime_ids()
    assert len(anime_ids) > 0

def test_set_name(test_user_builder):
    test_user_builder.from_login('laiscarraro').set_user_information()
    test_user_builder.set_name()
    assert test_user_builder.name == test_user_builder.user_information.user_name.values[0]

def test_build(test_user_builder):
    user = test_user_builder.from_login('laiscarraro').build()
    assert (
        isinstance(user, User) and
        user.get_login() == 'laiscarraro'
    )

def test_build_not_found(test_user_builder):
    user = test_user_builder.from_login('banana').build()
    assert (
        not isinstance(user, User) and
        user is None
    )
    