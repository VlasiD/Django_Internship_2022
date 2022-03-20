from rest_framework.serializers import ModelSerializer
from cities.models import Country, City


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'