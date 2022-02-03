from django.utils.deprecation import MiddlewareMixin
from cities.models import City


class CountryPopulationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        top10_countries = City.objects.all().order_by('-population')[:10]
        request.top10_countries = top10_countries