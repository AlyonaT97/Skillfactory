from .models import Category, Post, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['theme']


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('headline', 'article_text')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ['comment_text']
