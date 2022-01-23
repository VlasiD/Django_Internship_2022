from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from cities.models import Country, City


def countries(request):
    countries = Country.objects.all()
    return render(request, 'cities/countries.html', context={'countries': countries})


def country(request, pk):
    cities = City.objects.filter(country_id=pk)
    return render(request, 'cities/country.html', context={'cities': cities})


def city(request, pk, id):
    city = get_object_or_404(City, id=id)
    return render(request, 'cities/city.html', context={'city': city})