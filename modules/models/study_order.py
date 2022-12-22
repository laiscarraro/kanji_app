import pandas as pd

class StudyOrder():

    def __init__(self, unlocked_kanji, dependencies, kanji_order):
        self.unlocked_kanji = unlocked_kanji
        self.dependencies = dependencies
        self.kanji_order = kanji_order
    
    def get_unlocked_sentences(self):
        all_kanji = self.kanji_order[['Kanji']]

        locks = self.unlocked_kanji.merge(
            all_kanji, on='Kanji', how='right'
        )

        locks['has_unlocked'] = locks['Suggested Order'].fillna('').apply(
            lambda K: 1 if K != '' else 0
        )
        locks['has_locked'] = locks['Suggested Order'].fillna('').apply(
            lambda K: 0 if K != '' else 1
        )


        all_chars = pd.DataFrame(
            self.dependencies.kanji_vectorizer.get_feature_names_out(),
            columns=['Kanji']
        )

        locks_full = all_chars.merge(
            locks, on='Kanji', how='left'
        )

        has_unlocked = self.dependencies.bag_of_kanji.multiply(
            locks_full['has_unlocked'].fillna(0).apply(float).values
        )
        has_locked = self.dependencies.bag_of_kanji.multiply(
            locks_full['has_locked'].fillna(0).apply(float).values
        )

        has_unlocked_score = has_unlocked.sum(axis=1)
        has_locked_score = has_locked.sum(axis=1)

        unlocked_sentences = self.dependencies.subtitles
        unlocked_sentences['has_unlocked_score'] = has_unlocked_score
        unlocked_sentences['has_locked_score'] = has_locked_score

        return unlocked_sentences[
            (unlocked_sentences['has_unlocked_score'] > 0) &
            (unlocked_sentences['has_locked_score'] == 0)
        ]
