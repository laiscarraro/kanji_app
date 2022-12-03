from modules import session
import pytest

# Fixtures

@pytest.fixture
def test_session():
    return session.Session()


# Tests

def test_set_user_not_found(test_session):
    user_before = test_session.user
    user_found = test_session.set_user('banana')
    user_after = test_session.user

    assert (
        user_before is None and
        user_after is None and
        not user_found
    )

def test_set_user(test_session):
    user_before = test_session.user
    user_found = test_session.set_user('laiscarraro')
    user_after = test_session.user

    assert (
        user_before is None and
        user_after is not None and
        user_found
    )
    test_session.set_user(None)

def test_get_user(test_session):
    user_before = test_session.get_user()
    test_session.set_user('laiscarraro')
    user_after = test_session.get_user()

    assert (
        user_before is None and
        user_after is not None and
        user_after.get_login() == 'laiscarraro'
    )
