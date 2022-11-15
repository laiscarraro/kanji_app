from crawlers.crawler_interface import CrawlerInterface
from crawlers.utils import get_parsed_page

# External libs
import requests, os, re
import numpy as np
import pandas as pd
import time
from bs4 import BeautifulSoup

# Internal files
import data.fetch as fetch
from utils import extract_zip

class Subtitles(CrawlerInterface):

    def is_anime_link(link):
        has_strong = '<strong>' in str(link)
        return has_strong

    
    def anime_name(link):
        link_text = link.contents[0]
        lower_text = str(link_text).lower()
        clean_name = re.sub('</?strong>', '', lower_text)
        return clean_name


    def filter_anime_names(self, webpage):
        links = webpage.find_all('a')
        anime_links = filter(self.is_anime_link, links)
        return [
            (re.sub('</?strong>', '', str(i.contents[0]).lower()), i['href']) 
            for i in anime_links
        ]


    def get_anime_list(self, url):
        webpage = get_parsed_page(url)
        anime_list = pd.DataFrame([
            (re.sub('</?strong>', '', str(i.contents[0]).lower()), i['href']) 
            for i in webpage.find_all('a') if '<strong>' in str(i)
            ], columns=['name', 'path']
        )

        return anime_list


    def get_item_list(self, anime):
        try:
            path = np.array(fetch.animes_df[fetch.animes_df.name == anime.lower()]['path'])[0]
        except:
            print('anime not found :/')
            return

        page = requests.get('https://kitsunekko.net'+path)
        soup = BeautifulSoup(page.text, 'html.parser')

        names = [i.contents[0].lower() for i in soup.find_all('strong')]
        links = [i['href'] for i in soup.find_all('a') if '.srt' in str(i['href']) or '.rar' in str(i['href']) or '.zip' in str(i['href']) or '.7z' in str(i['href'])]

        return names, links


    def get_item_content(self, links, names):
        textos = []
        for l in range(len(links)):
            url = '%20'.join(('https://kitsunekko.net/'+links[l]).split())
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