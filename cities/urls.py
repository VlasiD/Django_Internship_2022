from django.urls import path, include
from cities.views import countries, country

urlpatterns = [
    path('countries/', countries, name='countries'),
    path('country/<int:pk>/', country, name='country'),
]

