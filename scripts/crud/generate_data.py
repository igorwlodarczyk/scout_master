import random
from const import *


def generate_date(year_range: tuple) -> str:
    year = random.randint(year_range[0], year_range[1])
    month = random.randint(1, 12)
    if month < 10:
        month = "0" + str(month)
    day = random.randint(1, 27)
    if day < 10:
        day = "0" + str(day)
    return f"{year}-{month}-{day}"


def load_countries(file):
    query = "INSERT INTO countries (name) VALUES\n"
    for index, country in enumerate(countries):
        if index == len(countries) - 1:
            query += f"    ('{country}');\n"
        else:
            query += f"    ('{country}'),\n"
    file.write(query)


def load_league_laliga(file):
    # Adding spanish league only
    query = "INSERT INTO leagues (name, country_id) VALUES ('LaLiga', 1);\n"
    file.write(query)


def load_clubs(file):
    # Adding clubs from spanish league only
    query = "INSERT INTO clubs (name, league_id) VALUES\n"
    for index, club in enumerate(laliga_clubs):
        if index == len(countries) - 1:
            query += f"    ('{club}', 1);\n"
        else:
            query += f"    ('{club}', 1),\n"
    file.write(query)


def load_players(file):
    query = "INSERT INTO players (first_name, last_name, birth_date, height, weight, nationality_id, role, club_id) VALUES\n"
    total_amount_of_players = 0
    for index, club in enumerate(laliga_clubs, start=1):
        number_of_players = random.randint(23, 27)
        for player in range(number_of_players):
            total_amount_of_players += 1
            first_name = random.choice(names)
            last_name = random.choice(last_names)
            birth_date = generate_date((1985, 2007))
            height = round(random.uniform(165, 202), 1)
            weight = round(height - 107 + round(random.uniform(0, 4), 1), 1)
            nationality = random.randint(1, len(countries))
            role = random.choice(football_roles)
            club_id = index
            query += f"    ('{first_name}', '{last_name}', '{birth_date}', {height}, {weight}, {nationality}, '{role}', {club_id}),\n"
    query += "    ('Igor', 'Wlodarczyk', '2000-07-27', 171.5, 67.8, 1, 'Forward', 1);\n"
    file.write(query)
    return total_amount_of_players


def load_games(file, number_of_games):
    query = "INSERT INTO games (date, home_club_id, away_club_id, result) VALUES\n"
    home_club_id = random.randint(1, len(laliga_clubs))
    while True:
        away_club_id = random.randint(1, len(laliga_clubs))
        if home_club_id != away_club_id:
            break
    result = f"{random.randint(0, 4)}-{random.randint(0, 4)}"
    for _ in range(number_of_games):
        game_date = generate_date((2023, 2024))
        query += f"    ('{game_date}', {home_club_id}, {away_club_id}, '{result}'),\n"
    query += f"    ('2023-07-27', 1, 2, '3-3');\n"
    file.write(query)


def load_reports(file, number_of_reports, number_of_games, total_amount_of_players):
    query = "INSERT INTO scout_reports (player_id, game_id, rating, minutes_played) VALUES\n"
    for _ in range(number_of_reports):
        player_id = random.randint(1, total_amount_of_players)
        game_id = random.randint(1, number_of_games)
        rating = round(random.uniform(1, 10), 1)
        minutes_played = random.randint(5, 90)
        query += f"    ({player_id}, {game_id}, {rating}, {minutes_played}),\n"
    query += f"    (1, 1, 7.0, 75);\n"
    file.write(query)


with open("load_data.sql", "w") as sql_file:
    number_of_games = 190
    number_of_reports = 100
    load_countries(sql_file)
    load_league_laliga(sql_file)
    load_clubs(sql_file)
    total_amount_of_players = load_players(sql_file)
    load_games(sql_file, number_of_games)
    load_reports(sql_file, number_of_reports, number_of_games, total_amount_of_players)
