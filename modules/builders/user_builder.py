from modules.user import User
from modules.builders.anime_builder import AnimeBuilder
import pandas as pd

class UserBuilder():
    
    def __init__(self):
        self.users_df = pd.read_csv('data/users.csv', sep=';')
        self.user_anime_df = pd.read_csv('data/user_anime.csv', sep=';')
        self.user_information = None
        
        self.id = None
        self.name = None
        self.login = None
        self.animes = []
    
    @staticmethod
    def get_user():
        return UserBuilder()
    
    def from_login(self, login):
        self.login = login
        return self
    
    def set_user_information(self):
        self.user_information = self.users_df[
            self.users_df.user_login == self.login
        ]
    
    def user_found(self):
        return len(self.user_information) > 0
    
    def set_id(self):
        self.id = self.user_information.user_id.values[0]
    
    def get_anime_ids(self):
        return self.user_anime_df[
            self.user_anime_df.user_id == self.id
        ].anime_id
    
    def set_name(self):
        self.name = self.user_information.user_name.values[0]

    def set_animes(self):
        anime_ids = self.get_anime_ids()
        self.animes = [
            AnimeBuilder.get_anime().from_id(id).build()
            for id in anime_ids
        ]
    
    def build(self):
        self.set_user_information()

        if self.user_found():
            self.set_id()
            self.set_name()
            self.set_animes()

            return User(
                id = self.id,
                name = self.name,
                login = self.login,
                animes = self.animes
            )
        
        else:
            return None