import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from ankipandas import Collection

class AnkiManager():

    def __init__(self, user_login):
        self.user_login = user_login
        self.user_decks = pd.read_csv('data/user_decks.csv', sep=';')
        self.kanji_decks = None
        self.word_decks = None
        self.fetch_user_decks()
        self.make_cards()
    
    def fetch_kanji_decks(self):
        kanji_decks = self.user_decks[
            (self.user_decks.user_login == self.user_login) &
            (self.user_decks.type == 'kanji')
        ]
        if len(kanji_decks) > 0:
            self.kanji_decks = kanji_decks.deck.values[0].split('|')
        
    def fetch_word_decks(self):
        word_decks = self.user_decks[
            (self.user_decks.user_login == self.user_login) &
            (self.user_decks.type == 'word')
        ]
        if len(word_decks) > 0:
            self.word_decks = word_decks.deck.values[0].split('|')

    def fetch_user_decks(self):
        self.fetch_kanji_decks()
        self.fetch_word_decks()
    
    def get_user_decks(self):
        return self.user_decks[
            self.user_decks.user_login == self.user_login
        ]

    def make_cards(self):
        col = Collection()
        metadata = col.cards
        metadata.index = metadata.nid
        data = col.notes

        self.cards = pd.merge(
            metadata, data,
            left_index=True, right_index=True
        )
    
    def get_cards(self):
        return self.cards
    
    def get_kanji_cards(self):
        kanji_cards = self.cards[
            self.cards.cdeck.apply(
                lambda a: a in self.kanji_decks
            )
        ]
        kanji_cards['kanji'] = kanji_cards['nflds'].apply(
            lambda a: a[0]
        )
        kanji_cards['meaning'] = kanji_cards['nflds'].apply(
            lambda a: a[1]
        )
        return kanji_cards 
    
    def get_word_cards(self):
        word_cards = self.cards[
            self.cards.cdeck.apply(
                lambda a: a in self.word_decks
            )
        ]
        word_cards['word'] = word_cards[['nflds', 'cdeck']].apply(
            (lambda a:
                re.sub('\[(\w|;|,)+]|</?div>|<br>', '', a[0][0])
                if '4' not in a[1]
                else re.sub('\[(\w|;|,)+]|</?div>|<br>', '', a[0][1])
            ), axis=1
        )
        word_cards['reading'] = word_cards[['nflds', 'cdeck']].apply(
            (lambda a:
                re.sub('</?div>|<br>', '', a[0][0])
                if '4' not in a[1]
                else re.sub('</?div>|<br>', '', a[0][1])
            ), axis=1
        )
        word_cards['meaning'] = word_cards[['nflds', 'cdeck']].apply(
            (lambda a:
                re.sub('\[(\w|;|,)+]|</?div>|<br>', '', a[0][1])
                if '4' not in a[1]
                else re.sub('\[(\w|;|,)+]|</?div>|<br>', '', a[0][2])
            ), axis=1
        )
        word_cards = word_cards.reset_index(drop=True)
        return word_cards 
    
    def get_available_decks(self):
        return self.cards.cdeck.unique()
    
    def set_kanji_decks(self, kanji_decks):
        self.kanji_decks = kanji_decks
        not_this_user_decks = self.user_decks[
            (self.user_decks.user_login != self.user_login) |
            (
                (self.user_decks.user_login == self.user_login) &
                (self.user_decks.type != 'kanji')
            )
        ]
        new_line = pd.DataFrame(
            [(self.user_login, 'kanji', '|'.join(kanji_decks))],
            columns=self.user_decks.columns
        )
        new_user_decks = pd.concat(
            [not_this_user_decks, new_line],
            ignore_index=True
        )

        self.user_decks = new_user_decks
        self.user_decks.to_csv('data/user_decks.csv', sep=';', index=False)
        return True

    def set_word_decks(self, word_decks):
        self.word_decks = word_decks
        not_this_user_decks = self.user_decks[
            (self.user_decks.user_login != self.user_login) |
            (
                (self.user_decks.user_login == self.user_login) &
                (self.user_decks.type != 'word')
            )
        ]
        new_line = pd.DataFrame(
            [(self.user_login, 'word', '|'.join(word_decks))],
            columns=self.user_decks.columns
        )
        new_user_decks = pd.concat(
            [not_this_user_decks, new_line],
            ignore_index=True
        )

        self.user_decks = new_user_decks
        self.user_decks.to_csv('data/user_decks.csv', sep=';', index=False)
        return True
    
    def get_kanji_decks(self):
        return self.kanji_decks

    def get_word_decks(self):
        return self.word_decks

    def get_bag_of_words(self):
        word_cards = self.get_word_cards()
        cv = CountVectorizer(token_pattern='(?u)\\b\w+\\b')
        bag_of_words = cv.fit_transform(word_cards.word)
        return cv, bag_of_words
    
    def get_words_metadata(self, cv, bag_of_words):
        word_cards = self.get_word_cards()
        words = pd.DataFrame(
            cv.get_feature_names(), columns=['Word']
        )
        words['index'] = words.index

        rows = bag_of_words.nonzero()[0]
        cols = bag_of_words.nonzero()[1]
        words['Type'] = words['index'].apply(
            lambda a: ' / '.join(word_cards.loc[
                rows[cols == a]
            ].cqueue.unique())
        )
        words['Sentences'] = words['index'].apply(
            lambda a: ' / '.join(word_cards.loc[
                rows[cols == a]
            ].reading.values)
        )
        words['Meaning'] = words['index'].apply(
            lambda a: ' / '.join(word_cards.loc[
                rows[cols == a]
            ].meaning.values)
        )
        words['Decks'] = words['index'].apply(
            lambda a: ' / '.join(word_cards.loc[
                rows[cols == a]
            ].cdeck.unique())
        )
        words = words[words['Word'].apply(lambda a: re.sub('\d+', '', a) != '')]
        words = words.drop(columns=['index'])
        return words.reset_index(drop=True)
    
    def get_words(self):
        cv, bag_of_words = self.get_bag_of_words()
        metadata = self.get_words_metadata(cv, bag_of_words)
        return metadata

    def get_unlocked_words(self):
        words = self.get_words()
        unlocked_words = words[
            words['Type'] != 'new'
        ]
        return unlocked_words['Word'].values
    
    def get_unlocked_kanji(self):
        kanji_cards = self.get_kanji_cards()
        unlocked_kanji = kanji_cards[
            kanji_cards['cqueue'] != 'new'
        ]
        return unlocked_kanji.kanji.values