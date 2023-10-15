from django.contrib import admin
from .models import Post, Category, Author, Comment
from modeltranslation.admin import TranslationAdmin


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'rating')


class PostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'post_time', 'post_author', 'rating', 'preview')
    list_filter = ('post_time', 'post_author', 'rating')
    search_fields = ('post_author', 'rating')



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['theme']
    list_filter = ['theme']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'rating')
    list_filter = ('comment_text', 'rating')



class CategoriesAdmin(TranslationAdmin):
    model = Category


class PostsAdmin(TranslationAdmin):
    model = Post


class CommentsAdmin(TranslationAdmin):
    model = Comment


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)






