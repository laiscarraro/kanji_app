import pandas as pd

class User:

    def __init__(self, id, name, login, animes, kanji):
        self.id = id
        self.name = name
        self.login = login
        self.animes = animes
        self.kanji = kanji

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
    
    def get_login(self):
        return self.login

    def get_animes(self):
        return self.animes
    
    def get_kanji(self):
        return self.kanji
    
    def set_animes(self, animes):
        self.animes = animes
    
    def count_animes(self):
        return len(self.animes)
    
    def get_animes_df(self):
        if self.count_animes() == 0:
            return None
        
        anime_data = [
            (anime.get_id(), anime.get_name()) 
            for anime in self.animes
        ]
        
        anime_df = pd.DataFrame(
            anime_data, columns=['id', 'name']
        )
        
        return anime_df
    
    def has_anime(self, anime_id):
        if self.count_animes() > 0:
            ids = self.get_animes_df().id.values
            return anime_id in ids
        else:
            return False
    
    def get_unified_subtitles(self):
        unified_subtitles = None
        for anime in self.animes:
            unified_subtitles = pd.concat(
                [unified_subtitles, anime.get_subtitles()],
                ignore_index=True
            )
        return unified_subtitles
    
    def update_kanji(self, kanji):
        user_kanji = pd.read_csv('data/user_kanji.csv', sep=';')
        not_this_user = user_kanji[
            user_kanji.user_id != self.get_id()
        ]
        new_kanji = pd.DataFrame(
            [(self.get_id(), kanji)],
            columns=user_kanji.columns
        )
        self.kanji = kanji
        final_df = pd.concat(
            [not_this_user, new_kanji],
            ignore_index=True
        )
        final_df.to_csv('data/user_kanji.csv', sep=';', index=None)