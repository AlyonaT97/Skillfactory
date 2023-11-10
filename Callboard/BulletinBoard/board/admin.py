from django.contrib import admin
from .models import Category, Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('headline', 'date_post', 'author_post', 'category_post')
    list_filter = ('date_post', 'author_post')
    search_fields = ['author_post']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('date_comment', 'author_comment', 'post_comment')
    list_filter = ('date_comment', 'author_comment', 'post_comment')
    search_fields = ('author_comment', 'post_comment')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)


