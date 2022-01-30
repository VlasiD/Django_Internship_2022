from django.urls import path, include
from cities.views import countries, country, city, create_country, create_city, edit_city, edit_country, \
    CitiesLoginView, CitiesLogoutView, register, delete_country, delete_city
from django.conf.urls.static import static
from Django_Internship_2022 import settings

urlpatterns = [
                  path('countries/', countries, name='countries'),
                  path('register/', register, name='register'),
                  path('login/', CitiesLoginView.as_view(), name='login'),
                  path('logout/', CitiesLogoutView.as_view(), name='logout'),
                  path('countries/add/', create_country, name='create_country'),
                  path('country/<int:pk>/edit/', edit_country, name='edit_country'),
                  path('country/<int:pk>/delete/', delete_country, name='delete_country'),
                  path('country/<int:pk>/', country, name='country'),
                  path('country/<int:pk>/add/', create_city, name='create_city'),
                  path('country/<int:pk>/<int:id>/', city, name='city'),
                  path('country/<int:pk>/<int:id>/edit/', edit_city, name='edit_city'),
                  path('country/<int:pk>/<int:id>/delete/', delete_city, name='delete_city'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
