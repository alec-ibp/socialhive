from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from socialhive.common.infrastructure.api.views import CustomModelViewSet

from socialhive.feed.application.post import PostManager
from socialhive.feed.domain.dtos import NewPostDTO
from socialhive.feed.infrastructure.api.serializers import PostSerializer
from socialhive.feed.infrastructure.repository.service import PostServiceRepository


class PostViewSet(CustomModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        if self.request.query_params.get('user'):
            queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('-published')

    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_dto = NewPostDTO(**serializer.validated_data, user=request.user)
        new_post = PostManager(PostServiceRepository()).create_post(post_dto)
        serialized_user = self.get_serializer(new_post)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)
