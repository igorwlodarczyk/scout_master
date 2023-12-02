import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from scouting.models import Player, Country, League, Club


class Command(BaseCommand):
    help = "Loads data into database"

    def add_arguments(self, parser):
        parser.add_argument("input_file", type=str, help="Input file with data")

    def handle(self, *args, **options):
        input_file_path = options["input_file"]

        with open(input_file_path, "r") as file:
            data = json.load(file)

        countries = self.__collect_countries(data)
        country_objects = [
            self.__create_country_object(country, flag_file_path)
            for country, flag_file_path in countries.items()
        ]

        league_objects = self.__create_league_objects(data, country_objects)
        club_objects = self.__create_club_objects(data, league_objects)
        player_objects = self.__create_player_objects(
            data, country_objects, club_objects
        )

    @staticmethod
    def __create_country_object(country_name, flag_file_path) -> Country:
        new_country = Country(name=country_name)
        with open(flag_file_path, "rb") as file:
            new_country.flag.save(
                os.path.basename(flag_file_path),
                File(file),
            )
        return new_country

    @staticmethod
    def __collect_countries(data):
        countries = {}
        for league in data["leagues"]:
            if league["country"]["country"] not in countries.keys():
                countries[league["country"]["country"]] = league["country"][
                    "country_file_path"
                ]
        for player in data["players"]:
            if player["nationality"]["nationality"] not in countries.keys():
                countries[player["nationality"]["nationality"]] = player["nationality"][
                    "nationality_file_path"
                ]
        return countries

    @staticmethod
    def __create_league_objects(data, country_objects):
        league_objects = []
        for league in data["leagues"]:
            for country in country_objects:
                if country.name == league["country"]["country"]:
                    league_country = country

            new_league = League(name=league["name"], country=league_country)
            with open(league["logo_path"], "rb") as file:
                new_league.logo.save(
                    os.path.basename(league["logo_path"]),
                    File(file),
                )
            league_objects.append(new_league)
        return league_objects

    @staticmethod
    def __create_club_objects(data, league_objects):
        club_objects = []
        for club in data["clubs"]:
            for league in league_objects:
                if league.name == club["league"]:
                    club_league = league

            new_club = Club(name=club["name"], league=club_league)
            with open(club["logo_path"], "rb") as file:
                new_club.badge.save(
                    os.path.basename(club["logo_path"]),
                    File(file),
                )
            club_objects.append(new_club)
        return club_objects

    def __create_player_objects(self, data, country_objects, club_objects):
        player_objects = []
        for player in data["players"]:
            for country in country_objects:
                if country.name == player["nationality"]["nationality"]:
                    player_country = country

            for club in club_objects:
                if club.name == player["club"]:
                    player_club = club

            new_player = Player(
                name=player["name"],
                birth_date=player["birth_date"],
                height=player["height"],
                nationality=player_country,
                position=player["position"],
                club=player_club,
            )
            with open(player["photo_path"], "rb") as file:
                new_player.photo.save(
                    os.path.basename(player["photo_path"]),
                    File(file),
                )
            player_objects.append(new_player)
        return player_objects
