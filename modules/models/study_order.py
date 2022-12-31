import pandas as pd

class StudyOrder():

    def __init__(self, dependencies, unlocked_kanji=None, kanji_order=None, unlocked_words=None, anki_words=None):
        self.unlocked_kanji = unlocked_kanji
        self.unlocked_words = unlocked_words
        self.dependencies = dependencies
        self.kanji_order = kanji_order
        self.anki_words = anki_words
        self.unlocked_sentences = None

    def get_unlocked_sentences_kanji(self):
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

        self.unlocked_sentences = unlocked_sentences[
            (unlocked_sentences['has_unlocked_score'] > 0) &
            (unlocked_sentences['has_locked_score'] == 0)
        ]
        return self.unlocked_sentences
    
    def get_unlocked_sentences_words(self):
        self.dependencies.make_bag_of_words()
        self.dependencies.bag_of_words
    
        all_words = self.anki_words[['Word']]

        locks = self.unlocked_words.merge(
            all_words, on='Word', how='right'
        )

        locks['has_unlocked'] = locks['index'].fillna('').apply(
            lambda K: 1 if K != '' else 0
        )
        locks['has_locked'] = locks['index'].fillna('').apply(
            lambda K: 0 if K != '' else 1
        )


        all_subs_words = pd.DataFrame(
            self.dependencies.word_vectorizer.get_feature_names_out(),
            columns=['Word']
        )

        locks_full = all_subs_words.merge(
            locks, on='Word', how='left'
        )

        has_unlocked = self.dependencies.bag_of_words.multiply(
            locks_full['has_unlocked'].fillna(0).apply(float).values
        )
        has_locked = self.dependencies.bag_of_words.multiply(
            locks_full['has_locked'].fillna(0).apply(float).values
        )

        has_unlocked_score = has_unlocked.sum(axis=1)
        has_locked_score = has_locked.sum(axis=1)

        unlocked_sentences = self.dependencies.subtitles
        unlocked_sentences['has_unlocked_score'] = has_unlocked_score
        unlocked_sentences['has_locked_score'] = has_locked_score

        self.unlocked_sentences = unlocked_sentences[
            (unlocked_sentences['has_unlocked_score'] > 0) &
            (unlocked_sentences['has_locked_score'] == 0)
        ]
        return self.unlocked_sentences
    
    def get_unlocked_sentences(self, type='kanji'):
        if type == 'kanji':
            return self.get_unlocked_sentences_kanji()
        else:
            return self.get_unlocked_sentences_words()
    
    def get_longest_subsequency(self, arr):
        n = len(arr)
        arr = arr + [-1]
    
        ans_list = []
        lista_provisoria = []
        for i in range(1, n+1):
            if arr[i]-arr[i-1] == 1:
                lista_provisoria.append(arr[i-1])
            else:
                lista_provisoria.append(arr[i-1])
                if len(lista_provisoria) > len(ans_list):
                    ans_list = lista_provisoria
                lista_provisoria = []
    
        return ans_list
    
    def get_unlocked_sequences(self, type='kanji'):
        self.get_unlocked_sentences(type=type)
        sentences = self.unlocked_sentences.drop_duplicates(
            subset=['anime_name', 'content']
        )
        sentences['index'] = sentences.index
        grouped = sentences.groupby(['anime_name', 'filename'])['index'].apply(list).reset_index()
        grouped['seq'] = grouped['index'].apply(self.get_longest_subsequency)
        grouped['n_seq'] = grouped['seq'].apply(len)
        sequences = grouped.sort_values(by='n_seq', ascending=False)[[
            'anime_name', 'filename', 'seq', 'n_seq'
        ]]
        sequences['content'] = sequences['seq'].apply(
            (
                lambda a: '\n'.join(sentences.loc[a].content.values)
            )
        )
        sequences['start_time'] = sequences['seq'].apply(
            (
                lambda a: min(sentences.loc[a].start_time.values)
            )
        )
        return sequences
