import requests
from bs4 import BeautifulSoup


def get_parsed_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup
