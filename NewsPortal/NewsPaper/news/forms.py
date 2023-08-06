from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    article_text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'headline',
            'article_text',
            'post_author',
            'post_category'
        ]

