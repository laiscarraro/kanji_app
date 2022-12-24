from modules.crawlers import utils
import pytest

# Fixtures

@pytest.fixture
def url():
    return 'https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F'

@pytest.fixture
def link(url):
    webpage = utils.get_parsed_page(url)
    links = webpage.find_all('a')
    return links[4]

@pytest.fixture
def link_content():
    return '<strong>Test Anime</strong>'


# Tests

def test_extract_root(url):
    assert utils.extract_root(url) == 'https://kitsunekko.net/'


def test_get_parsed_page(url):
    assert utils.get_parsed_page(url) is not None


def test_clean_content(link_content):
    assert utils.clean_content(link_content) == 'Test Anime'


def test_extract_content(link):
    assert utils.extract_content(link) == '.hack g.u'