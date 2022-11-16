import pandas as pd

class DataManager():

    def __init__(self):
        self.tables = dict()
        self.tables_read = []

    def update_tables_read(self):
        self.tables_read = list(self.tables.keys())

    def read_table(self, table_name):
        path = 'data/' + table_name + '.csv'
        dataframe = pd.read_csv(path, sep=';')
        self.tables[table_name] = dataframe
        self.update_tables_read()
    

    def query(self, table_name, query):
        if table_name not in self.tables_read:
            self.read_table(table_name)
        table = self.tables[table_name]
        return table.query(query)