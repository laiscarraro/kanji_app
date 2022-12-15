from sklearn.feature_extraction.text import CountVectorizer
from janome.tokenizer import Tokenizer
import pandas as pd

class WordOrder():

    def __init__(self, kanji_order, subtitles):
        self.kanji_order = kanji_order
        self.subtitles = subtitles
    
    def tokenize(self, doc):
        t = Tokenizer(wakati=True)
        tokenized = []
        for token in t.tokenize(doc):
            tokenized.append(str(token))
        return tokenized
    
    def get_word_df(self):
        tokenized_words = self.tokenize(
            self.subtitles.content.str.cat(sep=' ')
        )
        word_df = pd.DataFrame(set(tokenized_words), columns=['word'])
        return word_df

    def make_bag_of_kanji(self):
        vectorizer = CountVectorizer(analyzer='char')
        bow = vectorizer.fit_transform(self.get_word_df().word)
        return vectorizer, bow
    
    def get_kanji_df(self, kanji_list):
        kanji_df = pd.DataFrame(
            kanji_list, columns=['Kanji']
        )
        return kanji_df

    def get_score_matrix(self):
        vec, bow = self.make_bag_of_kanji()
        kanji_df = self.get_kanji_df(vec.get_feature_names_out())
        weights = self.kanji_order.merge(kanji_df, how='right')['Suggested Order'].fillna(0).apply(float)
        return bow.multiply(weights)

    def make_word_scores(self):
        score_matrix = self.get_score_matrix()
        word_df = self.get_word_df()
        word_df['score'] = score_matrix.sum(axis=1)
        self.word_scores = word_df[
            word_df.score > 0
        ]
    
    def get_words_with_kanji(self, kanji):
        return self.word_scores[
            self.word_scores.word.apply(
                lambda word: [
                    kanji in word
                ]
            )
        ]
    
    def get_reference_words(self):
        self.make_word_scores()
        kanjis = self.kanji_order.Kanji.str.cat(sep='')

        references = dict()
        for kanji in kanjis:
            words = self.get_words_with_kanji(kanji)
            if len(words) > 0:
                ref = words[
                    words.score == min(words.score)
                ].word.values[0]
                references[kanji] = ref
            else:
                references[kanji] = None
        
        self.reference_words = pd.DataFrame(
            references, columns=['kanji', 'reference_word']
        )