from django.contrib import admin
from django.contrib.auth.models import User
from .models import Country, League, Club, Player, ScoutReport

# Register your models here.
admin.site.register(Country)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(Player)
admin.site.register(ScoutReport)
