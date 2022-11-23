class Anime:

    def __init__(self, anime_information):
        self.anime_information = anime_information
    
    
    def get_id(self):
        return self.anime_information.anime_id.values[0]
    

    def get_name(self):
        return self.anime_information.anime_name.values[0]