from modules.crawlers import subtitles
import pandas as pd

class SubtitleHandler():

    def __init__(self):
        self.subtitles_df = pd.read_parquet('data/subtitles.parquet')
        self.crawler = subtitles.Subtitles()
    
    def download_subtitles(self, anime_name):
        return self.crawler.get_subtitle_df(anime_name)
    
    def update_subtitles_df(self, new_df):
        self.subtitles_df = pd.concat(
            [self.subtitles_df, new_df],
            ignore_index=True
        )
        self.subtitles_df.to_parquet('data/subtitles.parquet', index=False)
    
    def get_subtitles(self, anime_name):
        if anime_name in self.subtitles_df.anime_name.values:
            return self.subtitles_df[
                self.subtitles_df.anime_name == anime_name
            ]
        else:
            new_df = self.download_subtitles(anime_name)
            self.update_subtitles_df(new_df)
            return new_df