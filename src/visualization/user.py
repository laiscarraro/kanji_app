import pandas as pd

class User:

    def __init__(self, user_information, animes):
        self.user_information = user_information
        self.animes = animes

    def get_id(self):
        return self.user_information.user_id.values[0]
    

    def get_name(self):
        return self.user_information.user_name.values[0]

    
    def get_login(self):
        return self.user_information.user_login.values[0]


    def get_animes(self):
        return self.animes