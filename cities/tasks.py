import smtplib
from Django_Internship_2022.celery import celery_app
from django.core.mail import send_mail
from Django_Internship_2022.config import email, password


@celery_app.task
def send_activation_notification(user_email):
    print('1111111')
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
    print('222222222')


@celery_app.task
def test(arg):
    print(arg)