from django.http import HttpResponse
from django.shortcuts import render, redirect


def countries(request):
    data = ['Ukraine', 'USA', 'China', 'Germany']
    context = {'countries': data}
    return render(request, 'cities/countries.html', context=context)


def country(request, pk):
    data = {
        1: {
            'Kyiv': 1000,
            'Kharkiv': 650,
            'Cherkassy': 78,
            'Odessa': 350,
            'Lviv': 250,
            'Poltava': 90,
            'Sumy': 150,
            'Uzhgorod': 120,
            'Rivne': 520,
            'Zaporizhzhya': 600,
            'Dnipro': 750,
            'Lutsk': 400,
        },
        2: {'Chicago': 1000,
            'New York': 330,
            'Denver': 620,
            'Washington': 440},
        3: {'Pekin': 8250,
            'Shanhai': 1402,
            'Guandzoy': 2500},
        4: {'Berlin': 520,
            'Drezden': 83,
            'Munchen': 93},
    }
    context = {'country': data.get(pk)}
    return render(request, 'cities/cities.html', context=context)
