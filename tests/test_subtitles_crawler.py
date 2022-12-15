from modules.crawlers import subtitles
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
        len(anime_df.anime_name.values) > 0
    )


def test_filter_anime(subtitle_crawler, anime):
    filtered = subtitle_crawler.filter_anime(anime)
    assert (
        len(filtered) == 1 and
        filtered['anime_name'].values[0] == anime.lower()
    )


def test_anime_in_df(subtitle_crawler, anime):
    assert subtitle_crawler.anime_in_df(anime)


def test_get_path(subtitle_crawler, anime, path):
    assert (
        subtitle_crawler.get_path(anime) == path and
        subtitle_crawler.get_path('anime fake') == None
    )


def test_get_anime_page(subtitle_crawler, anime):
    webpage = subtitle_crawler.get_anime_page(anime)
    assert webpage is not None


def test_is_subtitle_file_link(subtitle_crawler):
    not_subtitle_file_link = 'teste.txt'
    subtitle_file_links = [
        'teste.srt',
        'teste.rar',
        'teste.zip'
        'teste.7z'
    ]
    assert (
        not subtitle_crawler.is_subtitle_file_link(not_subtitle_file_link)
        and sum([
            subtitle_crawler.is_subtitle_file_link(file)
            for file in subtitle_file_links
        ]) == len(subtitle_file_links)
    )


def test_get_subtitle_file_links(subtitle_crawler, anime):
    webpage = subtitle_crawler.get_anime_page(anime)
    subtitle_files = subtitle_crawler.get_subtitle_file_links(webpage)
    assert len(subtitle_files) > 0


def test_get_subtitle_file_name(subtitle_crawler, anime):
    webpage = subtitle_crawler.get_anime_page(anime)
    subtitle_file = subtitle_crawler.get_subtitle_file_links(webpage)[0]
    name = subtitle_crawler.get_subtitle_file_name(subtitle_file)
    assert name == '(hi10) shigatsu wa kimi no uso - (bd 720p) (lns-tsundere).japanese.7z'


def test_get_subtitle_file_link(subtitle_crawler, anime):
    webpage = subtitle_crawler.get_anime_page(anime)
    subtitle_file = subtitle_crawler.get_subtitle_file_links(webpage)[0]
    link = subtitle_crawler.get_subtitle_file_link(subtitle_file)
    assert link == 'https://kitsunekko.net/subtitles/japanese/Shigatsu_Wa_Kimi_No_Uso/(Hi10)_Shigatsu_wa_Kimi_no_Uso_-_(BD_720p)_(LNS-Tsundere).Japanese.7z'


def test_get_subtitle_files(subtitle_crawler, anime):
    names, links = subtitle_crawler.get_subtitle_files(anime)
    assert (
        len(names) == len(links)
        and len(names) > 0
    )


def test_get_subtitle_files_df(subtitle_crawler, anime):
    subtitle_files_df = subtitle_crawler.get_subtitle_files_df(anime)
    assert (
        len(subtitle_files_df) > 0 and
        subtitle_files_df['anime_name'].values[0] == anime
    )


def test_is_zip_file(subtitle_crawler):
    not_zip_file = 'file.srt'
    zip_file = 'file.rar'
    assert (
        not subtitle_crawler.is_zip_file(not_zip_file)
        and subtitle_crawler.is_zip_file(zip_file)
    )


def test_download_subtitle_files(subtitle_crawler, anime):
    subtitle_files_df = subtitle_crawler.get_subtitle_files_df(anime)
    subtitle_content, filenames = subtitle_crawler.download_subtitle_files(subtitle_files_df)
    assert (
        len(subtitle_content) == len(filenames) and
        len(subtitle_content) > 0
    )


def test_get_subtitle_df(subtitle_crawler, anime):
    subtitle_df = subtitle_crawler.get_subtitle_df(anime)
    assert (
        len(subtitle_df) > 0
        and subtitle_df['anime_name'].values[0] == anime
    )