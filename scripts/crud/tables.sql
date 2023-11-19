CREATE TABLE countries (
    id serial PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

CREATE TABLE leagues (
    id serial PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE
);

CREATE TABLE clubs (
    id serial PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    league_id INTEGER REFERENCES leagues(id) ON DELETE CASCADE
);

CREATE TABLE players (
    id serial PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    nationality_id INTEGER REFERENCES countries(id) ON DELETE CASCADE,
    role VARCHAR(255) NOT NULL,
    club_id INTEGER REFERENCES clubs(id) ON DELETE CASCADE
);

CREATE TABLE games (
    id serial PRIMARY KEY,
    date DATE NOT NULL,
    home_club_id INTEGER REFERENCES clubs(id) ON DELETE CASCADE,
    away_club_id INTEGER REFERENCES clubs(id) ON DELETE CASCADE,
    result VARCHAR(255) NOT NULL
);

CREATE TABLE scout_reports (
    id serial PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
    rating FLOAT NOT NULL,
    minutes_played INTEGER
);
