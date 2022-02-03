from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from cities.models import City


@receiver(post_save, sender=City)
def increase_population(sender, instance, created, *args, **kwargs):
    if created:
        instance.country.population += instance.population
        instance.country.save()
    else:
        all_cities = City.objects.filter(country_id=instance.country.id)
        total_population = sum([city.population for city in all_cities])
        instance.country.population = total_population
        instance.country.save()


@receiver(post_delete, sender=City)
def decrease_population(sender, instance, *args, **kwargs):
    instance.country.population -= instance.population
    instance.country.save()


