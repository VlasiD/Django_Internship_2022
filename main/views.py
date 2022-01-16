from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    return HttpResponse("Hello. It's a home page")


def text(request, arg):
    return HttpResponse('You entered route "%s"' % arg)


def sum(request, arg1, arg2):
    return HttpResponse("Sum: %d + %d = %d" % (arg1, arg2, arg1 + arg2))


def redirect_view(request):
    return redirect('home')


def profile(request, *args, **kwargs):
    return HttpResponse('User profile page')


def profile_update(request):
    return HttpResponse('Profile update page')


def register(request):
    return HttpResponse('Page for registration')
