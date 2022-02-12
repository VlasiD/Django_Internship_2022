from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from cities.models import Country, City
from cities.forms import CountryForm, CityForm, SearchForm, CustomUserCreationForm
from cities.tasks import send_activation_notification


def home(request):
    return redirect(request, 'countries')


def countries(request):
    countries = Country.objects.get_queryset().order_by('-population')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        countries = countries.filter(name__icontains=keyword)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(countries, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return render(request, 'cities/countries.html', context={'countries': countries, 'page': page, 'form': form})


def country(request, pk):
    country = get_object_or_404(Country, id=pk)
    cities = City.objects.filter(country_id=pk).order_by('-population')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        cities = cities.filter(name__icontains=keyword)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(cities, 15)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'cities': cities, 'country': country, 'page': page, 'form': form}
    return render(request, 'cities/country.html', context=context)


def city(request, pk, id):
    city = get_object_or_404(City, id=id)
    return render(request, 'cities/city.html', context={'city': city})


@login_required(login_url='/login/')
def create_country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CountryForm()
        return render(request, 'cities/create_country.html', context={'form': form})


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def edit_country(request, pk):
    country = get_object_or_404(Country, id=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            form.save()
            return redirect('countries')
    else:
        form = CountryForm(instance=country)
        return render(request, 'cities/edit_country.html', context={'form': form, 'country': country})


@login_required(login_url='/login/')
def edit_city(request, pk, id):
    city = get_object_or_404(City, id=id)
    if request.method == 'POST':
        form = CityForm(data=request.POST, instance=city)
        if form.is_valid():
            form.save()
            return redirect('country', city.country.id)
    else:
        form = CityForm(instance=city)
        return render(request, 'cities/edit_city.html', context={'form': form, 'city': city})


@login_required(login_url='/login/')
def delete_country(request, pk):
    country = get_object_or_404(Country, id=pk)
    if request.user.is_staff:
        country.delete()
    return redirect('countries')


@login_required(login_url='/login/')
def delete_city(request, pk, id):
    city = get_object_or_404(City, id=id)
    country_id = city.country.id
    if request.user.is_staff:
        city.delete()
    return redirect('country', country_id)


class CitiesLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('countries')


class CitiesLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'account/logout.html'


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            send_activation_notification.delay(new_user.email, new_user.username)
            return redirect('countries')
    return render(request, 'account/register_user.html', context={'form': form})
