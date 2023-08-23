from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post
from NewsPaper import settings


def send_notifications(pk):
    post = Post.object.get(pk=pk)
    categories = post.post_category.all()
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.subscribers.all()
    subscribers_emails = [s.email for s in subscribers]

    html_content = render_to_string(
        'email_created.html',
        {
            'post': post.preview(),
            'link': f'{settings.SITE_URL}posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новая статья уже на сайте',
        body=post.article_text,
        from_email=settings.EMAIL_HOST_USER,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

