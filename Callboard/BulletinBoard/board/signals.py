from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings


def send_notifications(pk, headline):
    html_content = render_to_string(
        'email_created.html',
        {
            'headline': headline,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новое объявление уже на сайте',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.DEFAULT_FROM_EMAIL,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


