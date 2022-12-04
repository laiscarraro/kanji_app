from modules.crawlers import kanji

from collections import Counter
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler

class KanjiOrder():

    def __init__(self, anime_list):
        self.kanji_crawler = kanji.Kanji()
        self.anime_list = anime_list
        self.possible_features = [
            'Strokes', 'Grade',
            'On Ratio with Proper Nouns',
            'Left Entropy', 'Right Entropy'
        ]

        self.features = self.possible_features
        self.target = 'Heisig_order'
    
    def get_possible_features(self):
        return self.possible_features
    
    def set_features(self, features):
        self.features = features
    
    # TODO escrever essa função
    def make_unified_subtitles(self):
        self.unified_subtitles = None

    # TODO escrever essa função
    def make_kanji_frequency_in_animes(self):
        all_subtitles = self.unified_subtitles.content.str.cat(sep=';')
        self.kanji_frequency_in_animes = Counter(all_subtitles)
    
    def make_kanji_data(self):
        self.kanji_data = pd.merge(
            self.kanji_crawler.kanji_database,
            self.kanji_frequency_in_animes, on='Kanji', how='left'
        ).fillna(0)
    
    def split_dataset(self):
        X = self.kanji_data[self.features + ['Radical Freq.']]
        y = self.kanji_data[self.target]

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
    
    def train(self):
        self.pipeline = Pipeline(steps=[
            ('Scaler', StandardScaler()),
            ('ElasticNet', ElasticNet(random_state=42))
        ])
        self.pipeline.fit(self.x_train, self.y_train)
    
    def make_coeficients(self):
        self.coeficients = self.pipeline['ElasticNet'].coef_
    
    def make_new_features(self):
        self.new_features = self.features + ['Frequency in animes']
    
    def transform_model_to_anime(self):
        self.anime_model = pd.DataFrame(
            StandardScaler().fit_transform(
                self.kanji_data[self.new_features]
            ), columns=self.new_features
        )
    
    def replace_frequency_to_anime(self):
        for feature in self.new_features:
            if feature == 'Frequency in animes':
                self.anime_model[feature] *= self.coeficients[
                    self.features.index('Radical Freq.')
                ]
                continue
            self.anime_model[feature] *= self.coeficients[
                self.features.index(feature)
            ]

    def make_suggested_order(self):
        self.anime_model['Kanji importance'] = self.anime_model[self.new_features].sum(axis=1)
        self.anime_model['Kanji'] = self.kanji_data['Kanji']
        suggested_order = pd.DataFrame(self.anime_model.sort_values(by='Kanji importance')['Kanji'])
        suggested_order['suggested_order'] = list(range(1, len(self.kanji_crawler.kanji_database)+1))
        self.suggested_order = suggested_order
    
    def get_kanji_order(self, features):
        self.set_features(features)
        self.make_unified_subtitles()
        self.make_kanji_frequency_in_animes()
        self.make_kanji_data()
        self.split_dataset()
        self.train()
        self.make_coeficients()
        self.make_new_features()
        self.transform_model_to_anime()
        self.replace_frequency_to_anime()
        self.make_suggested_order()
        return self.suggested_order