from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
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


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

