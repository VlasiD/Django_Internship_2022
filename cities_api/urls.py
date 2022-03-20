from django.urls import path
from cities_api import views

urlpatterns = [
    path('countries/', views.CountryListApiView.as_view()),
              ]