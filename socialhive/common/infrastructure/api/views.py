from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .pagination import CustomPagination
from .serializers import HiveUserSerializer
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
        return Response(serialized_user.data, status=201)
