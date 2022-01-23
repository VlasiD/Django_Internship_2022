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
