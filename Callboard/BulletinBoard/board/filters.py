from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
    headline = CharFilter(lookup_expr='icontains', label='По заголовку')
    date_post = DateFilter(
        lookup_expr='gt',
        field_name='date_post',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='По категории',
        empty_label='Любой'
    )

    class Meta:
        model = Post
        fields = [
            'headline',
            'date_post',
            'category'
        ]
