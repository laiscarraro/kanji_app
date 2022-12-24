from modules.managers.kanji_recommendation_manager import KanjiRecommendationManager
from modules.models.content_dependencies import ContentDependencies
from modules.models.study_order import StudyOrder
from modules.session import Session

import pytest

# Fixtures

@pytest.fixture
def study():
    session = Session()
    session.set_user('laiscarraro')
    user = session.get_user()

    recommender = KanjiRecommendationManager(user)
    kanji_order = recommender.get_latest_model()

    kanji_data = kanji_order[
        kanji_order.Kanji == kanji_order.Kanji.values[0]
    ].fillna('')
    n_unlocked_kanji = kanji_data['Suggested Order'].values[0]
    unlocked_kanji = kanji_order.iloc[:n_unlocked_kanji]
    dependencies = ContentDependencies(user.get_unified_subtitles())
    study = StudyOrder(unlocked_kanji, dependencies, kanji_order)

    return study

# Tests

def test_get_unlocked_sentences(study):
    sents = study.get_unlocked_sentences()
    assert (
        len(sents) > 0 and
        len(sents.content.dropna()) > 0
    )