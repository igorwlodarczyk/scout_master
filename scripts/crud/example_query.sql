SELECT players.first_name, players.last_name, countries.name AS "country", clubs.name AS "club"
FROM players
JOIN countries on players.nationality_id = countries.id
JOIN clubs on players.club_id = clubs.id;

SELECT players.first_name, players.last_name, clubs.name AS "club", scout_reports.rating AS "rating", scout_reports.date
FROM players
JOIN scout_reports on players.id = scout_reports.player_id
JOIN clubs on players.club_id = clubs.id
WHERE rating > 5
ORDER BY rating DESC;