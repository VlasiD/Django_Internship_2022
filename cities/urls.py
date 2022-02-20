from django.contrib.auth.decorators import login_required
from django.urls import path, include
from cities.views import CustomLoginView, CustomLogoutView, register, CityView, CountryCreateView, \
    CityCreateView, CountryUpdateView, CityUpdateView, CountryDeleteView, CityDeleteView, CountriesListView, CountryView
from django.conf.urls.static import static
from Django_Internship_2022 import settings

urlpatterns = [
                  path('countries/', CountriesListView.as_view(), name='countries'),
                  path('register/', register, name='register'),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('logout/', CustomLogoutView.as_view(), name='logout'),
                  path('countries/add/', CountryCreateView.as_view(), name='create_country'),
                  path('country/<int:pk>/edit/', CountryUpdateView.as_view(), name='edit_country'),
                  path('country/<int:pk>/delete/', CountryDeleteView.as_view(), name='delete_country'),
                  path('country/<int:pk>/', CountryView.as_view(), name='country'),
                  path('country/<int:pk>/add/', CityCreateView.as_view(), name='create_city'),
                  path('country/<int:pk>/<int:id>/', CityView.as_view(), name='city'),
                  path('country/<int:pk>/<int:id>/edit/', CityUpdateView.as_view(), name='edit_city'),
                  path('country/<int:pk>/<int:id>/delete/', CityDeleteView.as_view(), name='delete_city'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
