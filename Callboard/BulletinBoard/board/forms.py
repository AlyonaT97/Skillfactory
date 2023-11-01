from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post, Category


class PostForm(forms.ModelForm):
    headline = forms.CharField(label='Заголовок')
    text_post = forms.CharField(widget=CKEditorUploadingWidget, label='Контент')
    category_post = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label='Категория')

    class Meta:
        model = Post
        fields =[
            'headline',
            'text_post',
            'category_post',
        ]

