from django.shortcuts import redirect
from datetime import datetime
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string
from .models import Post, Category


def send_mail_subscriber(request):
    post = Post(
        headline=request.POST['headline'],
        article_text=request.POST['article_text'],
    )
    post.save()

    # получаем наш html
    html_content = render_to_string(
        'email_created.html',
        {
            'text': post.preview(),
        }
    )

    # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
    msg = EmailMultiAlternatives(
        subject=f'{post.headline}',
        body=post.article_text,  # это то же, что и message
        from_email='Cyrenova.Alyona@yandex.ru',
        to=['cyrenova.al@gmail.com', 'cyrenova.alena@mail.ru'],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

    return redirect('/posts/')
