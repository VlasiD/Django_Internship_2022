from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'

    name = models.CharField(max_length=50)
    iso = models.CharField(max_length=2)
    population = models.IntegerField(default=0)
    flag = models.ImageField()

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name_plural = 'Cities'

    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    population = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    flag = models.ImageField()
    has_mcdonalds = models.BooleanField()

    def __str__(self):
        return self.name


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    description = models.CharField(max_length=100)
    icon = models.ImageField()
    temperature = models.CharField(max_length=100)
    feels_like = models.CharField(max_length=100)
    pressure = models.CharField(max_length=100)
    humidity = models.CharField(max_length=100)
    wind_speed = models.CharField(max_length=100)