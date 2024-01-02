from django.contrib import admin
from .models import Country, League, Club, Player, ScoutReport, Match

# Register your models here.
admin.site.register(Country)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Player)
admin.site.register(ScoutReport)
admin.site.register(Match)
