# type: ignore
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from .pagination import CustomPagination
from .serializers import HiveUserSerializer, ChangePasswordSerializer
from socialhive.common.dtos import UserRegisterDTO
from socialhive.common.application.user import UserServiceManager
from socialhive.common.infrastructure.repository import UserServiceRespository


class CustomModelViewSet(ModelViewSet):
    pagination_class = CustomPagination

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.all()


class HiveUserViewSet(CustomModelViewSet):
    serializer_class = HiveUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
    
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_dto = UserRegisterDTO(**serializer.validated_data)
        user = UserServiceManager(UserServiceRespository()).create_user(user_dto)
        serialized_user = self.get_serializer(user)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={status.HTTP_201_CREATED: None},
    )
    def change_password(self, request: Request, *args, **kwargs) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        new_password_confirmation = serializer.validated_data["new_password_confirmation"]

        # TODO improve robustness and manage apu exceptions, validate that the old pass really matches
        if new_password != new_password_confirmation:
            raise Exception("New password and confirmation don't match.")
        if old_password.lower() == new_password.lower():
            raise Exception("New password can't be the same as the old one.")

        UserServiceManager(UserServiceRespository()).change_password(request.user, new_password)

        return Response(status=status.HTTP_201_CREATED)
