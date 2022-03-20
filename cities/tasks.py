import smtplib
from django.template.loader import render_to_string
from Django_Internship_2022.celery import celery_app
from django.core.mail import EmailMultiAlternatives
from Django_Internship_2022.config import email, password
from cities.models import City, Weather
from cities.utilities import get_weather
from datetime import datetime, timedelta


@celery_app.task()
def send_activation_notification(user_email, username):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(email, password)

    html_body = render_to_string("email/email.html", context={'username': username})
    subject = 'Welcome to Country&City Service'
    msg = EmailMultiAlternatives(subject=subject, from_email=email, to=[user_email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()


@celery_app.task
def add_weather():
    cities = City.objects.all()
    for city in cities:
        weather = get_weather(city_name=city.name, country_code=city.country.iso)
        Weather.objects.create(
            city=city,
            created_at=datetime.now(),
            description=weather['description'],
            icon=weather['icon'],
            temperature=weather['temperature'],
            feels_like=weather['feels_like'],
            pressure=weather['pressure'],
            humidity=weather['humidity'],
            wind_speed=weather['wind_speed']
        )


@celery_app.task
def delete_old_entries():
    all_entries = Weather.objects.get_queryset().order_by('-created_at')
    old_entries = all_entries.filter(created_at__lte=datetime.now() - timedelta(days=7))
    for entry in old_entries:
        entry.delete()


@celery_app.task
def test():
    print('----------------------')
