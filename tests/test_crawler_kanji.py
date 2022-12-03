from modules.crawlers import kanji
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
    column = kanji_crawler.make_order_column()
    assert (
        len(column) > 0 and
        column[0] == 1 and
        column[-1] == len(column)
    )


def test_get_grade_order(kanji_crawler):
    normal_order = kanji_crawler.kanji_database[kanji_crawler.key]
    grade_order = kanji_crawler.get_grade_order()
    assert (
        len(grade_order) == len(normal_order)
        and len(grade_order) > 0
        and not grade_order.equals(normal_order)
    )


def test_get_strokes_order(kanji_crawler):
    normal_order = kanji_crawler.kanji_database[kanji_crawler.key]
    strokes_order = kanji_crawler.get_strokes_order()
    assert (
        len(strokes_order) == len(normal_order)
        and len(strokes_order) > 0
        and not strokes_order.equals(normal_order)
    )


def test_get_freq_order(kanji_crawler):
    normal_order = kanji_crawler.kanji_database[kanji_crawler.key]
    freq_order = kanji_crawler.get_freq_order()
    assert (
        len(freq_order) == len(normal_order)
        and len(freq_order) > 0
        and not freq_order.equals(normal_order)
    )


def test_get_heisig_order(kanji_crawler):
    grade_order = kanji_crawler.get_grade_order()
    heisig_order = kanji_crawler.get_heisig_order()
    assert (
        len(heisig_order) == len(grade_order)
        and len(heisig_order) > 0
        and not heisig_order.equals(grade_order)
    )


def test_get_kanji_order(kanji_crawler):
    normal_order = kanji_crawler.kanji_database[kanji_crawler.key]
    kanji_order = kanji_crawler.get_kanji_order()
    columns = list(kanji_order.columns)
    assert (
        len(kanji_order) == len(normal_order)
        and len(kanji_order) > 0
        and 'grade_order' in columns
        and 'freq_order' in columns
        and 'strokes_order' in columns
        and 'Heisig_order' in columns
    )