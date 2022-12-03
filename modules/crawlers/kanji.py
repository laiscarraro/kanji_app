# External libs
import pandas as pd

KANJI_METADATA_URL = 'https://raw.githubusercontent.com/laiscarraro/Kanji-study/main/kanji_database.csv'
HEISIG_ORDER_URL = 'https://raw.githubusercontent.com/laiscarraro/Kanji-study/main/heisig_order.csv'
KANJI_ALIVE_URL = 'https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv'

class Kanji():

    def __init__(self):
        self.key = 'Kanji'
        self.fetch_external_data()
        self.set_kanji_database()
    

    def fetch_external_data(self):
        self.kanji_metadata = pd.read_csv(KANJI_METADATA_URL, sep=';')
        self.heisig_order = pd.read_csv(HEISIG_ORDER_URL)
        self.kanji_alive = pd.read_csv(KANJI_ALIVE_URL)
    

    def set_kanji_database(self):
        self.kanji_database = pd.merge(
            self.kanji_metadata, self.heisig_order, 
            on=self.key
        )
    
    
    def get_kanji_sorted_by_col(self, col):
        return pd.DataFrame(
            self.kanji_database.sort_values(by=col)[self.key]
        )


    def make_order_column(self):
        column_size = len(self.kanji_database) + 1
        return list(
            range(1, column_size)
        )


    def get_grade_order(self):
        grade_order = self.get_kanji_sorted_by_col(['Grade', 'Strokes'])
        grade_order['grade_order'] = self.make_order_column()
        return grade_order


    def get_strokes_order(self):
        strokes_order = self.get_kanji_sorted_by_col('Strokes')
        strokes_order['strokes_order'] = self.make_order_column()
        return strokes_order
    

    def get_freq_order(self):
        freq_order = self.get_kanji_sorted_by_col('Kanji Frequency without Proper Nouns')
        freq_order['freq_order'] = self.make_order_column()
        return freq_order

    
    def get_heisig_order(self):
        heisig_order = self.get_kanji_sorted_by_col('Heisig_order')
        heisig_order['heisig_order'] = self.make_order_column()
        return heisig_order

    
    def get_kanji_order(self):
        grade_order = self.get_grade_order()
        strokes_order = self.get_strokes_order()
        freq_order = self.get_freq_order()

        kanji_order = pd.merge(
            pd.merge(
                pd.merge(
                    grade_order, strokes_order, on=self.key
                ), freq_order, on=self.key
            ), self.heisig_order, on=self.key
        )
        return kanji_order
