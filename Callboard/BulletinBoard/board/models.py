from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_category', args=[str(self.ok)])


class Post(models.Model):
    headline = models.CharField(max_length=64, verbose_name='Заголовок')
    text_post = RichTextUploadingField(verbose_name='Контент')
    author_post = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    date_post = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'Объявление "{self.headline}" в категории "{self.category_post}" от {self.author_post}'

    def get_absolute_url(self):
        return f'/{self.pk}'


class Comment(models.Model):
    text_comment = models.TextField(verbose_name='Текст')
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date_comment = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Комментарий')
    confirmation_comment = models.BooleanField(default=False, verbose_name='Подтверждение')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author_comment} оставил комментарий "{self.text_comment}" под постом "{self.post_comment}"'

    def get_absolute_url(self):
        return f'comments/{self.pk}'
