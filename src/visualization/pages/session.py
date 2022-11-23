import pandas as pd
import user
import anime

class Session:

    def __init__(self):
        self.users = pd.read_csv('data/users.csv', sep=';')
        self.user_anime = pd.read_csv('data/user_anime.csv', sep=';')
        self.animes = pd.read_csv('data/animes.csv', sep=';')


    def get_user_information(self, user_login):
        user_information = self.users[
            self.users.user_name == user_login
        ]
        return user_information

    
    def get_anime_ids(self, user_information):
        user_id = user_information.user_id.values[0]
        anime_ids = self.user_anime[
            self.user_anime.user_id == user_id
        ].anime_id
        return anime_ids

    
    def get_anime_information(self, anime_id):
        anime_information = self.animes[
            self.animes.anime_id == anime_id
        ]
        return anime_information


    def get_user_animes(self, user_information):
        anime_ids = self.get_anime_ids(user_information)
        animes_information = [
            self.get_anime_information(id)
            for id in anime_ids
        ]
        animes = [
            anime.Anime(anime_information)
            for anime_information in animes_information
        ]
        return animes


    def get_user(self, user_login):
        user_information = self.get_user_information(user_login)
        animes = self.get_user_animes(self.user_information)
        return user.User(
            user_information,
            animes
        )