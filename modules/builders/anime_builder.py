from modules.anime import Anime
from modules.subtitle_handler import SubtitleHandler
import pandas as pd

class AnimeBuilder():

    def __init__(self):
        self.animes_df = pd.read_csv('data/animes.csv', sep=';')
        self.subtitle_handler = SubtitleHandler()

        self.id = None
        self.name = None
        self.subtitles = None
    
    @staticmethod
    def get_anime():
        return AnimeBuilder()
    
    def from_id(self, id):
        self.id = id
        return self
    
    def get_anime_information(self):
        return self.animes_df[
            self.animes_df.anime_id == self.id
        ]
    
    def set_name(self):
        anime_information = self.get_anime_information()
        self.name = anime_information.anime_name.values[0]
    
    def set_subtitles(self):
        self.subtitles = self.subtitle_handler.get_subtitles(self.name)
    
    def build(self):
        self.set_name()
        self.set_subtitles()

        return Anime(
            id = self.id,
            name = self.name,
            subtitles=self.subtitles
        )