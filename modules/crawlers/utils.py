import requests, re
from bs4 import BeautifulSoup


def extract_root(url):
    return re.search('https?://.*/', url).group(0)


def get_parsed_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def clean_content(content):
    return re.sub('</?strong>', '', content)


def extract_content(link):
    content = link.contents[0]
    lower_content = str(content).lower()
    clean = clean_content(lower_content)
    return clean
