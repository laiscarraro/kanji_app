from modules.models import content_dependencies
import os
import pandas as pd
import pytest

# Fixtures

@pytest.fixture
def orderer():
    subtitles = pd.read_csv('data/subtitles.csv', sep=';')
    subtitles = subtitles[subtitles.anime_name == 'ousama ranking']
    return content_dependencies.ContentDependencies(subtitles)


# Tests
