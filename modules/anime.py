class Anime:

    def __init__(self, id, name, subtitles):
        self.id = id
        self.name = name
        self.subtitles = subtitles
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_subtitles(self):
        return self.subtitles