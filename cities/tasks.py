import smtplib
from time import sleep
from django.core.mail import send_mail

from Django_Internship_2022.celery import celery_app
from celery import shared_task

from Django_Internship_2022.config import email, password


@shared_task()
def send_activation_notification(user_email):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    send_mail(
        'Thank you for registration',
        'Hello, Thank you for joining us.',
        email,
        [user_email],
        fail_silently=False
    )
