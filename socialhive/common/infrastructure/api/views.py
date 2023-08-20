from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .pagination import CustomPagination
from .serializers import HiveUserSerializer, HiveUserRegisterSerializer, ChangePasswordSerializer
from socialhive.common.dtos import UserRegisterDTO
from socialhive.common.application.user import UserServiceManager
from socialhive.common.infrastructure.repository.services.user import UserServiceRepository


class CustomModelViewSet(ModelViewSet):
    pagination_class = CustomPagination

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.all()


class HiveUserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=HiveUserRegisterSerializer,
        responses={status.HTTP_201_CREATED: HiveUserRegisterSerializer},
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = HiveUserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_dto = UserRegisterDTO(**serializer.validated_data)
        user = UserServiceManager(UserServiceRepository()).create_user(user_dto)
        serialized_user = HiveUserRegisterSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)


class HiveUserViewSet(CustomModelViewSet):
    serializer_class = HiveUserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={status.HTTP_200_OK: None},
    )
    def change_password(self, request: Request, *args, **kwargs) -> Response:
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserServiceManager(UserServiceRepository()).change_password(request.user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated,))
    def me(self, request):
        model = self.get_serializer().Meta.model
        instance = model.objects.get(pk=request.user.id)
        return Response(self.get_serializer(instance).data)
