from modules.handlers.kanji_recommendation_handler import KanjiRecommendationHandler
from modules.crawlers import kanji
import pandas as pd

class KanjiRecommendationManager():

    def __init__(self, user):
        self.user = user
        self.subtitles = self.user.get_unified_subtitles()
        self.handler = KanjiRecommendationHandler()
        self.user_configuration = pd.read_csv('data/models/user_configuration.csv', sep=';')
    
    def get_animes_from_ids(self, anime_ids):
        all_animes = self.user.get_animes()
        selected_animes = [
            anime for anime in all_animes
            if anime.get_id() in anime_ids
        ]
        return selected_animes
    
    def get_subtitles_from_animes(self, selected_animes):
        names = [
            anime.get_name() 
            for anime in selected_animes
        ]
        selected_subs = self.subtitles[
            self.subtitles.anime_name.isin(names)
        ]
        return selected_subs
    
    def search_latest_model(self):
        return self.user_configuration[
            (self.user_configuration.model == 'kanji_order') &
            (self.user_configuration.user_login == self.user.get_login())
        ]
    
    def update_latest_model_metadata(self, filename):
        self.user_configuration = self.user_configuration[
            ~(
                (self.user_configuration.model == 'kanji_order') &
                (self.user_configuration.user_login == self.user.get_login())
            )
        ]
        new_line = pd.DataFrame(
            [(
                self.user.get_login(),
                'kanji_order',
                filename
            )], columns=self.user_configuration.columns
        )
        self.user_configuration = pd.concat(
            [self.user_configuration, new_line],
            ignore_index=True
        )
        self.user_configuration.to_csv('data/models/user_configuration.csv', sep=';', index=None)
    
    def handle_model_filename(self, anime_ids, features):
        anime_list = self.get_animes_from_ids(anime_ids)
        subtitles = self.get_subtitles_from_animes(anime_list)
        self.handler.set_anime_list(anime_list)
        self.handler.set_features(features)
        self.handler.set_subtitles(subtitles)
        return self.handler.get_model_filename()
    
    def make_default_model(self):
        anime_ids = self.user.get_animes_df().id.values
        features = self.handler.get_possible_features()
        filename = self.handle_model_filename(
            anime_ids, features
        )
        self.update_latest_model_metadata(filename)
    
    def get_latest_model_filename(self):
        latest_model_dataframe = self.search_latest_model()
        if len(latest_model_dataframe) == 0:
            self.make_default_model()
            latest_model_dataframe = self.search_latest_model()
        return latest_model_dataframe.filename.values[0]
    
    def update_latest_model(self, anime_ids, features):
        new_filename = self.handle_model_filename(
            anime_ids, features
        )
        current_filename = self.get_latest_model_filename()
        if new_filename != current_filename:
            self.update_latest_model_metadata(new_filename)
    
    def get_kanji_information(self, model):
        kanji_information = kanji.Kanji().kanji_alive
        return pd.merge(
            model, kanji_information,
            on='Kanji', how='inner'
        )
    
    def get_latest_model(self):
        latest_model_filename = self.get_latest_model_filename()
        model = pd.read_parquet(
            'data/models/' + latest_model_filename
        )
        return self.get_kanji_information(model)