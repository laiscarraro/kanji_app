from src import user
import pytest
import unittest

# Fixtures

@pytest.fixture
def example_user():
    return user.User('laiscarraro')


# Tests

def test_get_attribute(example_user):
    valid_attribute = 'user_id'
    assert example_user.get_attribute(valid_attribute) == 1