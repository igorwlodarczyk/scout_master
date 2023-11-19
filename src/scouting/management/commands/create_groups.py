from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Creates groups to identify users"

    def handle(self, *args, **options):
        groups = ["Scout", "Sports_director"]

        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
