from celery import shared_task

from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@shared_task
def notify_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    html_content = render_to_string(
        'email_created.html',
        {
            'headline': post.headline,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'На доске объявлений появилось новое объявление - {post.headline}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL]
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('Уведомление о новом объявлении отправлено на почту')