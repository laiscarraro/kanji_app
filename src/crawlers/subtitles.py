from src.crawlers.crawler_interface import CrawlerInterface

from src.crawlers.utils import get_parsed_page
from src.crawlers.utils import extract_content
from src.crawlers.utils import extract_root

# External libs
import requests, os
import numpy as np
import pandas as pd
import time

# Internal files
from src.utils import extract_zip

class Subtitles(CrawlerInterface):

    def __init__(self, url):
        self.url = url
        self.root = extract_root(url)
        self.anime_df = self.get_anime_df()


    def is_anime_link(self, link):
        has_strong = '<strong>' in str(link)
        return has_strong


    def extract_anime_links(self):
        webpage = get_parsed_page(self.url)
        links = webpage.find_all('a')
        anime_links = filter(self.is_anime_link, links)
        return list(anime_links)
    

    def make_anime_tuples(self, anime_links):
        anime_tuples = []

        for link in anime_links:
            name = extract_content(link)
            path = link['href']
            anime_tuples.append((name, path))

        return anime_tuples
    
    
    def get_animes(self):
        anime_links = self.extract_anime_links()
        anime_tuples = self.make_anime_tuples(anime_links)
        return anime_tuples
    

    def get_anime_df(self):
        anime_df = pd.DataFrame(
            self.get_animes(),
            columns=['name', 'path']
        )
        return anime_df


    def filter_anime(self, anime_name):
        return self.anime_df[
            self.anime_df.name == anime_name.lower()
        ]


    def anime_in_df(self, anime):
        filtered_df = self.filter_anime(anime)
        return len(filtered_df) > 0


    def get_path(self, anime):
        if self.anime_in_df(anime):
            filtered_df = self.filter_anime(anime)
            path = filtered_df['path'].values[0]
        else:
            path = None
        return path


    def get_list_from_anime(self, anime):
        path = self.get_path(anime)

        webpage = get_parsed_page(self.root+path)

        names = [i.contents[0].lower() for i in webpage.find_all('strong')]
        links = [
            i['href'] for i in webpage.find_all('a') 
            if '.srt' in str(i['href']) 
            or '.rar' in str(i['href']) 
            or '.zip' in str(i['href']) 
            or '.7z' in str(i['href'])
        ]

        return names, links


    def get_anime_content(self, links, names):
        textos = []
        for l in range(len(links)):
            url = '%20'.join((self.root+links[l]).split())
            print(url)
            if (
                '.zip'  in os.path.splitext(names[l])[1] or
                '.rar'  in os.path.splitext(names[l])[1] or
                '.7z'   in os.path.splitext(names[l])[1]
            ):
                [textos.append(i) for i in extract_zip(requests.get(url, stream=True))]
            else:
                textos.append(requests.get(url).text)
                time.sleep(0.05)
        
        try:
            print('gotten', len(textos), 'subs! check it out:', textos[0][:100])
        except:
            print('gotten', len(textos), 'subs! check it out:', textos)
        return textos