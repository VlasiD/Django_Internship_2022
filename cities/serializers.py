from django.contrib.auth.models import User
from rest_framework import serializers
from cities.models import Country, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'population', 'slug', 'flag', 'has_mcdonalds']
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password')