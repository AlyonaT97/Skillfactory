from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (Posts, PostCreate, PostDetail, PostEdit, PostDelete, Profile, Search,
                    Comments, CommentCreate, CommentDetail, confirm_comment, reject_comment)


urlpatterns = [
    path('', Posts.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),

    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('profile/', Profile.as_view(), name='profile'),

    path('filter/', Search.as_view(), name='search'),

    path('<int:pk>/create/', CommentCreate.as_view(), name='comment_create'),
    path('comments/', Comments.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('comments/<int:pk>/confirm/', confirm_comment, name='confirm_comment'),
    path('comments/<int:pk>/reject/', reject_comment, name='reject_comment'),
]