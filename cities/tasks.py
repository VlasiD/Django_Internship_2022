import smtplib
from django.template.loader import render_to_string
from Django_Internship_2022.celery import celery_app
from django.core.mail import send_mail, EmailMultiAlternatives
from Django_Internship_2022.config import email, password


@celery_app.task
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
