# External libs
import numpy as np
import pandas as pd

# Model imports
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler

# Internal files
import data.preprocess as preprocess

def anime_order(anime_freq_raw):
    anime_freq = pd.DataFrame(anime_freq_raw, columns=['Kanji', 'anime_freq'])
    df = pd.merge(preprocess.kanji_database, anime_freq, on='Kanji', how='left').fillna(0)

    features = ['Strokes', 'Grade', 'Radical Freq.', 'On Ratio with Proper Nouns', 'Left Entropy', 'Right Entropy']

    X = df[features]
    y = df['Heisig_order']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline(steps=[
                       ('Scaler', StandardScaler()),
                       ('ElasticNet', ElasticNet(random_state=42))
    ])

    pipe.fit(x_train, y_train)
    coefs = pipe['ElasticNet'].coef_

    new_features = ['Strokes', 'Grade', 'anime_freq', 'On Ratio with Proper Nouns', 'Left Entropy', 'Right Entropy']
    data_norm = pd.DataFrame(StandardScaler().fit_transform(df[new_features]), columns=new_features)

    for f in new_features:
        if f == 'anime_freq':
            data_norm[f] *= coefs[features.index('Radical Freq.')]
            continue
        data_norm[f] *= coefs[features.index(f)]

    data_norm['Kanji importance'] = data_norm[new_features].sum(axis=1)
    data_norm['Kanji'] = df['Kanji']
    suggested_order = pd.DataFrame(data_norm.sort_values(by='Kanji importance')['Kanji'])
    suggested_order['suggested_order'] = list(range(1, len(preprocess.kanji_database)+1))

    return suggested_order