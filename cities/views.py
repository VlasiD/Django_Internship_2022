from django.shortcuts import render, redirect, get_object_or_404
from cities.models import Country, City
from cities.forms import CountryForm, CityForm


def home(request):
    return redirect(request, 'countries')


def countries(request):
    countries = Country.objects.all()
    return render(request, 'cities/countries.html', context={'countries': countries})


def country(request, pk):
    country = get_object_or_404(Country, id=pk)
    cities = City.objects.filter(country_id=pk)
    return render(request, 'cities/country.html', context={'cities': cities, 'country': country})


def city(request, pk, id):
    city = get_object_or_404(City, id=id)
    return render(request, 'cities/city.html', context={'city': city})


def create_country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CountryForm()
        return render(request, 'cities/create_country.html', context={'form': form})


def create_city(request, pk):
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES)
        if form.is_valid():
            new_city = form.save(commit=False)
            new_city.country = get_object_or_404(Country, id=pk)
            new_city.save()
            return redirect('country', pk=pk)
    else:
        form = CityForm()
        return render(request, 'cities/create_city.html', context={'form': form})


def edit_country(request, pk):
    country = Country.objects.get(id=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CountryForm(instance=country)
        return render(request, 'cities/edit_country.html', context={'form': form, 'country': country})



def edit_city(request, pk, id):
    city = get_object_or_404(City, id=id)
    if request.method == 'POST':
        form = CityForm(data=request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('city', city.country.id, id)
    else:
        form = CityForm(instance=city)
        return render(request, 'cities/edit_city.html', context={'form': form, 'city': city})
