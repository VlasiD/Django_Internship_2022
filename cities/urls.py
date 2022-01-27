from django.urls import path, include
from cities.views import countries, country, city, create_country, create_city, edit_city, edit_country
from django.conf.urls.static import static
from Django_Internship_2022 import settings

urlpatterns = [
    path('countries/', countries, name='countries'),
    path('countries/add/', create_country, name='create_country'),
    path('country/<int:pk>/edit/', edit_country, name='edit_country'),
    path('country/<int:pk>/', country, name='country'),
    path('country/<int:pk>/add/', create_city, name='create_city'),
    path('country/<int:pk>/<int:id>/', city, name='city'),
    path('country/<int:pk>/<int:id>/edit/', edit_city, name='edit_city'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
