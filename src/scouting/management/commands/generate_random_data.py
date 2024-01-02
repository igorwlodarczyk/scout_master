import random
from django.core.management.base import BaseCommand
from django.db.models import Q
from scouting.models import Club, Match, Player, ScoutReport
from itertools import combinations
from datetime import datetime


def generate_date(start_year, end_year):
    year = random.randint(start_year, end_year)
    day = random.randint(1, 29)
    month = random.randint(1, 12)
    random_date = datetime(year, month, day).date()
    return random_date


def generate_result():
    home_club_score = random.randint(0, 5)
    away_club_score = random.randint(0, 4)
    return f"{home_club_score}:{away_club_score}"


def generate_match_objects():
    clubs = Club.objects.all()
    for club1, club2 in combinations(clubs, 2):
        random_date = generate_date(2019, 2023)
        match = Match.objects.create(
            date=random_date,
            home_club=club1,
            away_club=club2,
            result=generate_result(),
        )
        match.save()


def generate_scout_reports():
    players = Player.objects.all()
    for player in players:
        games = Match.objects.all().filter(
            Q(home_club=player.club) | Q(away_club=player.club)
        )
        for game in games:
            minutes_played = random.randint(60, 90)
            rating = round(random.uniform(5, 10), 1)
            report = ScoutReport(
                player=player,
                match=game,
                rating=rating,
                minutes_played=minutes_played,
                scout_name="JohnFlansky",
            )
            report.save()


class Command(BaseCommand):
    help = "Generates random Match and ScoutReport objects"

    def handle(self, *args, **options):
        Match.objects.all().delete()
        generate_match_objects()
        ScoutReport.objects.all().delete()
        generate_scout_reports()
