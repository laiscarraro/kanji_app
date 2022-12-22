import pandas as pd
import uuid
from modules.models import kanji_order

class KanjiRecommendationHandler():

    def __init__(self):
        self.possible_features = [
            'Strokes', 'Grade',
            'On Ratio with Proper Nouns',
            'Left Entropy', 'Right Entropy',
        ]
        self.features = self.possible_features
        self.anime_list = []
        self.subtitles = None
        self.metadata = pd.read_csv('data/models/metadata.csv', sep=';')
        self.metadata['anime_ids'] =  self.metadata['anime_ids'].apply(str)

    def get_possible_features(self):
        return self.possible_features
    
    def set_features(self, features):
        self.features = features
    
    def set_anime_list(self, anime_list):
        self.anime_list = anime_list
    
    def set_subtitles(self, subtitles):
        self.subtitles = subtitles

    def search_trained_model_filename(self):
        anime_ids = ','.join([
            str(anime.get_id()) for anime in self.anime_list
        ])
        features = ','.join(self.features)
        filename = self.metadata[
            (self.metadata.anime_ids == anime_ids) &
            (self.metadata.features == features)
        ].filename

        if len(filename) > 0:
            return filename.values[0]
        else:
            return None
        
    def update_metadata(self, filename):
        anime_ids = ','.join([
            str(anime.get_id()) for anime in self.anime_list
        ])
        features = ','.join(self.features)
        new_line = pd.DataFrame(
            [(filename, anime_ids, features)],
            columns=self.metadata.columns
        )
        self.metadata = pd.concat(
            [self.metadata, new_line],
            ignore_index=True
        )
        self.metadata.to_csv('data/models/metadata.csv', sep=';', index=None)
    
    def save_model(self, model):
        filename = 'kanji_order_' + str(uuid.uuid4()) + '.parquet'
        model.to_parquet(
            'data/models/' + filename
        )
        self.update_metadata(filename)
        return filename
    
    def train_model(self):
        model = kanji_order.KanjiOrder(self.subtitles, self.features)
        filename = self.save_model(
            model.get_kanji_order()
        )
        return filename
    
    def get_model_filename(self):
        trained_model_filename = self.search_trained_model_filename()
        if trained_model_filename is None:
            trained_model_filename = self.train_model()
        return trained_model_filename
