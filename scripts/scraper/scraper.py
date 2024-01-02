import requests
import re
import json
from bs4 import BeautifulSoup
from const import headers, timeout_time, photos_dir, months
from utils import download_image
from unidecode import unidecode


class Scraper(BeautifulSoup):
    def __init__(self, *args, **kwargs):
        self.__config = kwargs.pop("config")
        super().__init__(*args, **kwargs)

    def __get_player_links(self):
        url = self.__config["base_url"] + self.__config["players_url"]
        urls = [url] + self.__config["clubs"]
        for url in urls:
            html = self.__get_html(url)
            self.__update_html_to_be_parsed(html)

            elements = self.find_all("td", class_="hauptlink")
            for element in elements:
                a_tag = element.find("a")
                href = a_tag.get("href")
                if "profil" in href:
                    yield href

    @staticmethod
    def __get_html(url: str) -> str:
        return requests.get(url, headers=headers, timeout=timeout_time).text

    def __update_html_to_be_parsed(self, html: str):
        self.__dict__.update(
            Scraper(html, "html.parser", config=self.__config).__dict__
        )

    def run(self):
        links = self.__get_player_links()
        data = self.__get_data(links)
        with open("output.json", "w") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def __parse_name(name: str) -> str:
        parsed_name = re.sub(r"#\d+", "", name).strip()
        return unidecode(parsed_name)

    def __get_data(self, players_hrefs):
        data = {"players": [], "clubs": [], "leagues": []}
        seen_players = []
        # TODO: make it more clear
        for href in players_hrefs:
            player = {}
            url = self.__config["base_url"] + href
            if url not in seen_players:
                seen_players.append(url)
                html = self.__get_html(url)
                self.__update_html_to_be_parsed(html)
                name = self.find("h1", class_="data-header__headline-wrapper").text
                parsed_name = self.__parse_name(name)
                player["name"] = parsed_name
                photo_url = self.find("img", class_="data-header__profile-image").get(
                    "src"
                )
                photo_name = parsed_name.replace(" ", "_").lower() + ".jpg"
                photo_file_path = photos_dir / photo_name
                download_image(photo_url, headers, photo_file_path)
                player["photo_path"] = str(photo_file_path.resolve())
                nationality_element = self.find("span", {"itemprop": "nationality"})
                nationality = nationality_element.text.strip()
                nationality_file_url = nationality_element.find("img")["src"]
                nationality_file_name = nationality.lower() + ".png"
                nationality_file_path = photos_dir / nationality_file_name
                download_image(nationality_file_url, headers, nationality_file_path)
                nationality_dict = {
                    "nationality": nationality,
                    "nationality_file_path": str(nationality_file_path.resolve()),
                }
                player["nationality"] = nationality_dict
                height = int(
                    float(
                        self.find("span", {"itemprop": "height"})
                        .text.strip()
                        .replace(" m", "")
                        .replace(",", ".")
                    )
                    * 100
                )
                player["height"] = height
                birth_date = self.find("span", {"itemprop": "birthDate"}).text
                parsed_birth_date = self.__parse_date(birth_date)
                player["birth_date"] = parsed_birth_date
                position_element = self.find(
                    lambda tag: tag.name == "li" and "Position:" in tag.text
                )
                position = position_element.find("span").text.strip()
                player["position"] = position
                club_name = self.find("span", {"itemprop": "affiliation"}).text.strip()
                club_logo_url = self.__parse_club_logo_url(
                    self.find("a", class_="data-header__box__club-link").find("img")[
                        "srcset"
                    ]
                )
                club_logo_file_name = club_name.replace(" ", "").lower() + ".png"
                club_logo_file_path = photos_dir / club_logo_file_name
                download_image(club_logo_url, headers, club_logo_file_path)
                league_element = self.find("span", class_="data-header__league")
                league_name = unidecode(league_element.text.strip())
                league_logo_url = league_element.find("img")["src"]
                league_logo_file_name = league_name.replace(" ", "").lower() + ".png"
                league_logo_file_path = photos_dir / league_logo_file_name
                download_image(league_logo_url, headers, league_logo_file_path)
                league_country_element = self.find(
                    lambda tag: tag.name == "span" and "League level:" in tag.text
                ).find("img")
                league_country = league_country_element["title"]
                league_country_file_url = league_country_element["src"]
                league_country_file_name = (
                    league_country.replace(" ", "").lower() + ".png"
                )
                league_country_file_path = photos_dir / league_country_file_name
                league = {}
                league["name"] = league_name
                league["logo_path"] = str(league_logo_file_path.resolve())
                league_country_dict = {
                    "country": league_country,
                    "country_file_path": str(league_country_file_path.resolve()),
                }
                league["country"] = league_country_dict
                club = {}
                club["name"] = club_name
                club["league"] = league_name
                club["logo_path"] = str(club_logo_file_path.resolve())
                player["club"] = club_name
                download_image(
                    league_country_file_url, headers, league_country_file_path
                )
                data["players"].append(player)
                if club not in data["clubs"]:
                    data["clubs"].append(club)
                if league not in data["leagues"]:
                    data["leagues"].append(league)
        return data

    @staticmethod
    def __parse_club_logo_url(url: str) -> str:
        url = url.strip()
        return url.split(" ")[0]

    @staticmethod
    def __parse_date(date: str) -> str:
        date = re.sub(r"\(\d+\)", "", date)
        date = date.strip()
        month_day, year = date.split(", ")
        month, day = month_day.split(" ")
        date_string = f"{year}-{months[month]}-{day}"
        return date_string
