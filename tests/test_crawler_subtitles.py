from src.crawlers import subtitles
import pytest

# Fixtures

@pytest.fixture
def subtitle_crawler():
    return subtitles.Subtitles('https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F')

@pytest.fixture
def anime():
    return 'shigatsu wa kimi no uso'

@pytest.fixture
def path():
    return '/dirlist.php?dir=subtitles%2Fjapanese%2FShigatsu_Wa_Kimi_No_Uso%2F'

# Tests

def test_is_anime_link(subtitle_crawler):
    anime_link = '<strong>Anime Link</strong>'
    not_anime_link = '<a> no </a>'
    assert (
        not subtitle_crawler.is_anime_link(not_anime_link)
        and subtitle_crawler.is_anime_link(anime_link) 
    )


def test_extract_anime_links(subtitle_crawler):
    assert len(subtitle_crawler.extract_anime_links()) > 0


def test_make_anime_tuples(subtitle_crawler):
    links = subtitle_crawler.extract_anime_links()
    tuple_list = subtitle_crawler.make_anime_tuples(links)
    assert (
        len(tuple_list) > 0
        and len(tuple_list[0]) == 2
    )


def test_get_animes(subtitle_crawler):
    tuple_list = subtitle_crawler.get_animes()
    assert (
        len(tuple_list) > 0
        and len(tuple_list[0]) == 2
    )


def test_get_anime_df(subtitle_crawler):
    anime_df = subtitle_crawler.get_anime_df()
    assert (
        len(anime_df) > 0 and
        len(anime_df.columns) > 0 and
        len(anime_df.name.values) > 0
    )


def test_filter_anime(subtitle_crawler, anime):
    filtered = subtitle_crawler.filter_anime(anime)
    assert len(filtered) == 1


def test_anime_in_df(subtitle_crawler, anime):
    assert subtitle_crawler.anime_in_df(anime)


def test_get_path(subtitle_crawler, anime, path):
    assert (
        subtitle_crawler.get_path(anime) == path and
        subtitle_crawler.get_path('anime fake') == None
    )


def test_get_list_from_anime(subtitle_crawler):
    pass


def test_get_anime_content(subtitle_crawler):
    pass