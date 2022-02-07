from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from cities.models import Country, City


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        exclude = ['population']


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        exclude = ['country']


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, required=False, label='Search...')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)