from django.urls import path, include

from cities.views import CustomLoginView, CustomLogoutView, register, CityView, CountryCreateView, \
    CityCreateView, CountryUpdateView, CityUpdateView, CountryDeleteView, CityDeleteView, CountriesListView, \
    CountryView, CityListApiView, CityCreateApiView, CityUpdateApiView, CityApiView, CityDeleteApiView, CreateUserApiView
from django.conf.urls.static import static
from Django_Internship_2022 import settings

api_urlpatterns = [
    path('city/', CityListApiView.as_view(), name='api_city_list'),
    path('city/<int:pk>', CityApiView.as_view(), name='api_city_list'),
    path('country/<int:pk>/city/create/', CityCreateApiView.as_view(), name='api_city_create'),
    path('city/<int:pk>/update/', CityUpdateApiView.as_view(), name='api_city_update'),
    path('city/<int:pk>/delete/', CityDeleteApiView.as_view(), name='api_city_delete'),
    path('register/', CreateUserApiView.as_view(), name='register'),
]

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
      path('api/', include(api_urlpatterns))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATICFILES_DIRS)
