from src import data_manager

class User():

    def __init__(self, user_login):
        self.manager = data_manager.DataManager()
        self.data = self.manager.query(
            table_name='user',
            query = 'user_login == \"' + user_login + '\"'
        )
    

    def get_attribute(self, attribute):
        possible_attributes = list(self.data.columns)
        if attribute not in possible_attributes:
            raise ValueError(
                'Invalid attribute ' + attribute + '. Possible values are ' + str(possible_attributes)
            )
        else:
            return self.data[attribute].values[0]
        

    
    def get_animes(self):
        user_id = self.data.user_id.values[0]
        user_anime = self.manager.query(
            table_name='user_anime',
            query='user_id == ' + user_id
        )
        anime_ids = user_anime['anime_id'].values
        return self.manager.query(
            table_name='anime',
            query='anime_id in ' + anime_ids
        )

