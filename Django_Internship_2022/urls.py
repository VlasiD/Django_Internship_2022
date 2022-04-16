"""Django_Internship_2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cities import views

router = routers.DefaultRouter()
router.register(r'country/create', views.CountryCreateViewSet, basename='api_country_create')
router.register(r'country/update', views.CountryUpdateViewSet, basename='api_country_update')
router.register(r'country/delete', views.CountryDeleteViewSet, basename='api_country_delete')
router.register(r'country', views.CountriesListViewSet, basename='api_country_list')

urlpatterns = [
    path('', include('cities.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

