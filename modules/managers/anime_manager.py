import pandas as pd
from modules.builders import anime_builder

class AnimeManager():

    def __init__(self, user):
        self.animes_df = pd.read_parquet('data/animes.parquet')
        self.all_animes = pd.read_parquet('data/user_anime.parquet')
        self.user = user
        self.user_animes = self.all_animes[
            self.all_animes.user_id == user.get_id()
        ]
    
    def get_available_animes(self):
        if self.user.count_animes() > 0:
            return self.animes_df[
                ~self.animes_df.anime_id.isin(
                    self.user.get_animes_df().id
                )
            ]
        else:
            return self.animes_df
    
    def user_has_anime(self, anime_id):
        return self.user.has_anime(anime_id)

    def dataframe_has_anime(self, anime_id):
        return anime_id in self.user_animes.anime_id.values
    
    def new_anime(self, anime_id):
        builder = anime_builder.AnimeBuilder.get_anime()
        return builder.from_id(anime_id).build()
    
    def add_anime_to_user(self, anime_id):
        animes = self.user.get_animes()
        new_animes = animes + [self.new_anime(anime_id)]
        self.user.set_animes(new_animes)

    def add_anime_to_dataframe(self, anime_id):
        new_line = pd.DataFrame(
            [(self.user.get_id(), anime_id)],
            columns=self.all_animes.columns
        )
        new_dataframe = pd.concat(
            [self.all_animes, new_line],
            ignore_index=True
        )
        new_dataframe.to_parquet('data/user_anime.parquet', index=False)
    
    def add_anime(self, anime_id):
        added = False
        if not self.user_has_anime(anime_id):
            self.add_anime_to_user(anime_id)
            added = True
        if not self.dataframe_has_anime(anime_id):
            self.add_anime_to_dataframe(anime_id)
            added = True
        return added
        
    def remove_anime_from_user(self, anime_id):
        animes = self.user.get_animes()
        new_animes = [
            anime for anime in animes
            if anime.get_id() != anime_id
        ]
        self.user.set_animes(new_animes)
        
    def remove_anime_from_dataframe(self, anime_id):
        this_user = self.all_animes.user_id == self.user.get_id()
        this_anime = self.all_animes.anime_id == anime_id
        new_dataframe = self.all_animes[
            ~ this_user |
            (this_user & ~ this_anime)
        ]
        new_dataframe.to_parquet('data/user_anime.parquet', index=False)

    def remove_anime(self, anime_id):
        removed = False
        if self.user_has_anime(anime_id):
            self.remove_anime_from_user(anime_id)
            removed = True
        if self.dataframe_has_anime(anime_id):
            self.remove_anime_from_dataframe(anime_id)
            removed = True
        return removed