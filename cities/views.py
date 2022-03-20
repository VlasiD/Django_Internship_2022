from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from cities.models import Country, City, Weather
from cities.forms import CountryForm, CityForm, SearchForm, CustomUserCreationForm
from cities.tasks import send_activation_notification, test
from cities.utilities import duration


class CountriesListView(generic.ListView):
    template_name = 'cities/countries.html'
    model = Country
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(CountriesListView, self).get_context_data()
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
        else:
            keyword = ''
        context['form'] = SearchForm(initial={'keyword': keyword})
        return context

    def get_queryset(self):
        countries = super(CountriesListView, self).get_queryset().order_by('-population')
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            return countries.filter(name__icontains=keyword)
        return countries

    @method_decorator(decorator=duration, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super(CountriesListView, self).dispatch(request, *args, **kwargs)


class CountryView(generic.ListView):
    template_name = 'cities/country.html'
    model = City
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(CountryView, self).get_context_data()
        context['country'] = get_object_or_404(Country, id=self.kwargs['pk'])
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
        else:
            keyword = ''
        context['form'] = SearchForm(initial={'keyword': keyword})
        return context

    def get_queryset(self):
        cities = super(CountryView, self).get_queryset().filter(country_id=self.kwargs['pk']).order_by('-population')
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            return cities.filter(name__icontains=keyword)
        return cities

    @method_decorator(decorator=duration, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super(CountryView, self).dispatch(request, *args, **kwargs)


class CityView(generic.ListView):
    template_name = 'cities/city.html'
    model = City

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = get_object_or_404(City, id=self.kwargs['id'])
        context['city'] = city
        context['weather'] = Weather.objects.filter(city=city).order_by('-created_at')[0]
        return context


@method_decorator(login_required, name='dispatch')
class CountryCreateView(generic.CreateView):
    template_name = 'cities/create_country.html'
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy('countries')


@method_decorator(login_required, name='dispatch')
class CityCreateView(generic.CreateView):
    template_name = 'cities/create_city.html'
    model = City
    form_class = CityForm

    def form_valid(self, form):
        form.instance.country = Country.objects.get(id=self.kwargs['pk'])
        return super(CityCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('country', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class CountryUpdateView(generic.UpdateView):
    template_name = 'cities/edit_country.html'
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy('countries')


@method_decorator(login_required, name='dispatch')
class CityUpdateView(generic.UpdateView):
    template_name = 'cities/edit_city.html'
    model = City
    form_class = CityForm

    def get_object(self, queryset=None):
        return get_object_or_404(City, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse_lazy('country', kwargs={'pk': self.kwargs['pk']})


@method_decorator(login_required, name='dispatch')
class CountryDeleteView(generic.DeleteView, AccessMixin):
    template_name = 'cities/delete.html'
    model = Country
    success_url = reverse_lazy('countries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'country'
        country = get_object_or_404(Country, id=self.kwargs['pk'])
        context['object_name'] = country.name
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        else:
            return super(CountryDeleteView, self).dispatch(request)


@method_decorator(login_required, name='dispatch')
class CityDeleteView(generic.DeleteView, AccessMixin):
    template_name = 'cities/delete.html'
    model = City

    def get_object(self, queryset=None):
        return get_object_or_404(City, id=self.kwargs['id'])

    def get_success_url(self):
        messages.success(self.request, "Your preset has been deleted")
        return reverse_lazy('country', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'city'
        city = get_object_or_404(City, id=self.kwargs['id'])
        context['object_name'] = city.name
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        else:
            return super(CityDeleteView, self).dispatch(request)


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('countries')


class CustomLogoutView(LoginRequiredMixin, LogoutView):
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
