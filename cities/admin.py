from django.contrib import admin
from cities.models import Country, City


class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['country', 'has_mcdonalds']


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
