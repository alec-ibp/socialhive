from django.urls import path

from socialhive.feed.infrastructure.api.viewsets import PostViewSet


urlpatterns = [
    path('posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts'),
]
