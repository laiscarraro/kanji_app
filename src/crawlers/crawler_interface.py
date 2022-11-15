from abc import ABC, abstractmethod


class CrawlerInterface(ABC):

    @abstractmethod
    def get_anime_df(self, url: str):
        pass


    @abstractmethod
    def get_list_from_anime(self):
        pass


    @abstractmethod
    def get_anime_content(self, links, names):
        pass