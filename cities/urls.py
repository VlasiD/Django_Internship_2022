from django.urls import path, include
from cities.views import countries, country, city
from django.conf.urls.static import static
from Django_Internship_2022 import settings

urlpatterns = [
    path('countries/', countries, name='countries'),
    path('country/<int:pk>/', country, name='country'),
    path('country/<int:pk>/<int:id>', city, name='city'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
