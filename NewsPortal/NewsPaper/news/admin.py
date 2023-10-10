from django.contrib import admin
from .models import Post, Category, Author


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


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)

