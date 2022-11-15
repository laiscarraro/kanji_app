from src.crawlers import kanji
import pytest

# Fixtures

@pytest.fixture
def kanji_crawler():
    kanji_crawler = kanji.Kanji()
    return kanji_crawler


# Tests

def test_fetch_external_data(kanji_crawler):
    kanji_crawler.fetch_external_data()
    assert (
        len(kanji_crawler.kanji_metadata) > 0 and
        len(kanji_crawler.heisig_order) > 0 and
        len(kanji_crawler.kanji_alive) > 0
    )


def test_set_kanji_database(kanji_crawler):
    kanji_crawler.set_kanji_database()
    assert (
        len(kanji_crawler.kanji_database) > 0
    )


def test_get_kanji_sorted_by_col(kanji_crawler):
    stroke = kanji_crawler.get_kanji_sorted_by_col('Strokes')
    grade_stroke = kanji_crawler.get_kanji_sorted_by_col(['Grade', 'Strokes'])
    assert (
        len(stroke) == len(grade_stroke)
        and len(stroke) > 0
        and not stroke.equals(grade_stroke)
    )

def test_make_order_column(kanji_crawler):
    pass


def test_get_grade_order(kanji_crawler):
    pass


def test_get_strokes_order(kanji_crawler):
    pass


def test_get_freq_order(kanji_crawler):
    pass


def test_get_kanji_order(kanji_crawler):
    pass