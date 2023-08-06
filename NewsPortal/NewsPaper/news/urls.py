from django.urls import path
from .views import PostList, PostDetail,PostSearch, PostCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete')
]
