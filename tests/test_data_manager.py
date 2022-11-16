from src import data_manager
import pytest

# Fixtures

@pytest.fixture
def manager():
    return data_manager.DataManager()


# Tests

def test_update_tables_read(manager):
    before = manager.tables_read
    manager.tables = {
        'teste': 'teste'
    }
    manager.update_tables_read()
    after = manager.tables_read
    assert (
        len(before) == 0 and
        len(after) == 1
    )


def test_read_table(manager):
    manager.read_table('user')
    assert (
        manager.tables_read[-1] == 'user' and
        len(manager.tables['user']) > 0
    )


def test_query(manager):
    user = manager.query(
        table_name='user',
        query='user_login == \"laiscarraro\"'
    )
    assert (
        len(user) == 1 and
        user.user_login.values[0] == 'laiscarraro'
    )