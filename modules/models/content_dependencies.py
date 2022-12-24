from sklearn.feature_extraction.text import CountVectorizer

class ContentDependencies():

    def __init__(self, subtitles):
        self.subtitles = subtitles
        self.make_bag_of_kanji()
    
    def make_bag_of_kanji(self):
        self.kanji_vectorizer = CountVectorizer(analyzer='char')
        self.bag_of_kanji = self.kanji_vectorizer.fit_transform(
            self.subtitles.content.fillna('')
        )