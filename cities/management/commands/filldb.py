from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from cities.models import Country, City


class Command(BaseCommand):
    help = 'Fill the database by values'

    def handle(self, *args, **options):
        countries = [
            ['China', '1751', 'image.png'],
            ['Poland', '30', 'image.png'],
            ['Spain', '35', 'image.png'],
            ['Sweden', '80', 'image.png'],
            ['Finland', '40', 'image.png'],
            ['Australia', '150', 'image.png'],
        ]

        for item in countries:
            Country.objects.create(
                name=item[0],
                iso=item[0][:2],
                population=item[1],
                flag=item[1]
            )

        cities = {
            'China': [['Chizhou', 212, 'image.png', 'True'], ['Huangshan', 212, 'image.png', 'True']],
            'Poland': [['Warsaw', 15, 'image.png', 'True'], ['Wrocław', 10, 'image.png', 'True']],
            'Spain': [['Madrid', 30, 'image.png', 'True'], ['Barcelona', 40, 'image.png', 'True']],
            'Sweden': [['Kalmar', 20, 'image.png', 'True'], ['Lund', 7, 'image.png', 'True']],
            'Finland': [['Helsinki', 60, 'image.png', 'True'], ['Vanta', 22, 'image.png', 'True']],
            'Australia': [['Melbourne', 102, 'image.png', 'True'], ['Sydney', 122, 'image.png', 'True']]
        }

        for country in countries:
            data = cities[country[0]]
            for item in data:
                new_city = City.objects.create(
                    name=item[0],
                    population=item[1],
                    slug=item[0].lower(),
                    flag=item[2],
                    has_mcdonalds=item[3],
                    country=get_object_or_404(Country, name=country[0])
                )
                new_city.save()