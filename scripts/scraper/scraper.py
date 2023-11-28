import requests
from bs4 import BeautifulSoup


class Scraper(BeautifulSoup):
    def __init__(self, *args, **kwargs):
        self.__start_links = kwargs.pop("start_links")
        super().__init__(*args, **kwargs)
        self.__player_links = self.__get_player_links()

    def __get_player_links(self):
        elements = self.find_all("td", class_="hauptlink")
        for element in elements:
            a_tag = element.find("a")
            href = a_tag.get("href")
            if "profil" in href:
                yield href

    def __get_data(self):
        ...
