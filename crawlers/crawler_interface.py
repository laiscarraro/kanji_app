from abc import ABC, abstractmethod


class CrawlerInterface(ABC):

    @abstractmethod
    def get_anime_list(self, url: str):
        pass


    @abstractmethod
    def get_item_list(self):
        pass


    @abstractmethod
    def get_item_content(self, links, names):
        pass