from django.core.management import BaseCommand
from cities.tasks import add_weather


class Command(BaseCommand):
    help = 'Adds new weather entry for all cities in DB'

    def handle(self, *args, **options):
        add_weather()