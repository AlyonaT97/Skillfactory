from django.urls import path
from .views import (PostList, PostCreate, PostDetail, PostEdit)


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('edit/', PostEdit.as_view(), name='post_edit'),
]