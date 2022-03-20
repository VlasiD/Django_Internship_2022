from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cities.models import Country
from cities_api.serializers import CountrySerializer


class CountryListApiView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticated,)