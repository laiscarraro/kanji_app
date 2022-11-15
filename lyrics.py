# External libs
import requests, os, re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

# Internal files
import data.fetch as fetch
from utils import *

def get_anime_list(letter):
    page = requests.get('https://www.animelyrics.com/anime/_'+letter.upper())
    soup = BeautifulSoup(page.text, 'html.parser')
    anime_list = pd.DataFrame([
            (i.contents[0].lower(), i['href']) 
            for i in soup.find_all('a')
            if 'href' in i.attrs.keys()
            and re.match('anime/[a-z0-9]', str(i['href']))
        ], columns=['name', 'path']
    )

    return anime_list

def get_lyric_list(anime):
    try:
        path = np.array(fetch.data.animes_df[fetch.data.animes_df.name == anime.lower()]['path'])[0]
    except:
        print('anime not found :/')
        return

    page = requests.get('https://kitsunekko.net'+path)
    soup = BeautifulSoup(page.text, 'html.parser')

    names = [i.contents[0].lower() for i in soup.find_all('strong')]
    links = [i['href'] for i in soup.find_all('a') if '.srt' in str(i['href']) or '.rar' in str(i['href']) or '.zip' in str(i['href']) or '.7z' in str(i['href'])]

    return names, links

def get_lyrics(links, names):
    textos = []
    for l in range(len(links)):
        url = '%20'.join(('https://kitsunekko.net/'+links[l]).split())
        print(url)
        if '.zip' in os.path.splitext(names[l])[1] or '.rar' in os.path.splitext(names[l])[1] or '.7z' in os.path.splitext(names[l])[1]:
            [textos.append(i) for i in extract_zip(requests.get(url, stream=True))]
        else:
            textos.append(requests.get(url).text)
            time.sleep(0.05)
    
    try:
        print('gotten', len(textos), 'subs! check it out:', textos[0][:100])
    except:
        print('gotten', len(textos), 'subs! check it out:', textos)
    return textos