from modules.models import content_dependencies
from modules.session import Session
import pandas as pd
import pytest

# Fixtures

@pytest.fixture
def depend():
    session = Session()
    session.set_user('laiscarraro')
    user = session.get_user()
    return content_dependencies.ContentDependencies(
        user.get_unified_subtitles()
    )


# Tests

def test_make_bag_of_kanji(depend):
    assert depend.bag_of_kanji is not None