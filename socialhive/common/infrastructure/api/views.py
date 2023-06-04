# type: ignore
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema

from .pagination import CustomPagination
from .serializers import HiveUserSerializer, ChangePasswordSerializer
from socialhive.common.dtos import UserRegisterDTO
from socialhive.common.application.user import UserServiceManager
from socialhive.common.infrastructure.repository import UserServiceRepository


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
        user = UserServiceManager(UserServiceRepository()).create_user(user_dto)
        serialized_user = self.get_serializer(user)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={status.HTTP_200_OK: None},
    )
    def change_password(self, request: Request, *args, **kwargs) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        new_password_confirmation = serializer.validated_data["new_password_confirmation"]

        user = request.user
        
        coincidences: int = 0
        password_length: int = min(len(new_password), len(old_password))
        for i in range(password_length):
            if old_password[i].lower() == new_password[i].lower():
                coincidences += 1

        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect.")
        if new_password != new_password_confirmation:
            raise ValidationError("New password and confirmation don't match.")
        if old_password.lower() == new_password.lower():
            raise ValidationError("New password can't be the same as the old one.")
        if coincidences >= password_length // 2:
            raise ValidationError("New password can't be too similar to the old one.")

        UserServiceManager(UserServiceRepository()).change_password(request.user, new_password)

        return Response(status=status.HTTP_200_OK)
