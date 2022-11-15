# External libs
import pandas as pd

# Internal imports
from crawlers.subtitles import Subtitles

KANJI_METADATA_URL = 'https://raw.githubusercontent.com/laiscarraro/Kanji-study/main/kanji_database.csv'
HEISIG_ORDER_URL = 'https://raw.githubusercontent.com/laiscarraro/Kanji-study/main/heisig_order.csv'
KANJI_ALIVE_URL = 'https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv'
ANIME_SUBTITLES_URL = 'https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F'
ANIME_LYRICS_URL = 'https://www.animelyrics.com/anime/_'

# Kanji data

kanji_metadata = pd.read_csv(KANJI_METADATA_URL, sep=';')
heisig_order = pd.read_csv(HEISIG_ORDER_URL)
kanji_alive = pd.read_csv(KANJI_ALIVE_URL)

# Anime data

subtitles_crawler = Subtitles()
animes_df = subtitles_crawler.get_anime_list(ANIME_SUBTITLES_URL)