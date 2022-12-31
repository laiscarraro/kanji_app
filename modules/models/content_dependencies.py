from sklearn.feature_extraction.text import CountVectorizer
import MeCab

class ContentDependencies():

    def __init__(self, subtitles):
        self.subtitles = subtitles
        self.mecab = MeCab.Tagger('-Owakati')
        self.make_bag_of_kanji()
    
    def make_bag_of_kanji(self):
        self.kanji_vectorizer = CountVectorizer(analyzer='char')
        self.bag_of_kanji = self.kanji_vectorizer.fit_transform(
            self.subtitles.content.fillna('')
        )
    
    def mecab_analyzer(self, text):
        return self.mecab.parse(text).split()
    
    def make_bag_of_words(self):
        self.word_vectorizer = CountVectorizer(analyzer=self.mecab_analyzer)
        self.bag_of_words = self.word_vectorizer.fit_transform(
            self.subtitles.content.fillna('')
        )