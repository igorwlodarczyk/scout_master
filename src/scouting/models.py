from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=200)
    flag = models.ImageField(upload_to="scouting/files/flags")

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="scouting/files/league_logos")

    def __str__(self):
        return self.name


class Club(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    badge = models.ImageField(upload_to="scouting/files/club_badges")

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    height = models.IntegerField()
    photo = models.ImageField(upload_to="scouting/files/player_photos")
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.club.name}"


class Match(models.Model):
    date = models.DateField()
    home_club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="home_club"
    )
    away_club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="away_club"
    )
    result = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.home_club} {self.result} {self.away_club} - {self.date}"


class ScoutReport(models.Model):
    date = models.DateField(auto_now_add=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    rating = models.FloatField()
    minutes_played = models.IntegerField()
    scout_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.scout_name} - {self.player.name} - {self.match.date} - {self.rating}"
