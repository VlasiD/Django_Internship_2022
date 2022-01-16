from django.urls import path, include
from main.views import home, text, sum, redirect_view, profile, profile_update, register

account_url = [
    path('profile/', profile, name='profile'),
    path('update/', profile_update, name='profile_update'),
    path('register/', register, name='register'),
]

urlpatterns = [
    path('', home, name='home'),
    path('account/', include(account_url)),
    path('redirectroute/', redirect_view, name='redirect_rote'),
    path('<str:arg>/', text, name='text'),
    path('sum/<int:arg1>/<int:arg2>/', sum, name='sum'),
]

