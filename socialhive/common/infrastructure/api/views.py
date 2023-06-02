from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .pagination import CustomPagination
from .serializers import HiveUserSerializer
from socialhive.common.infrastructure.db.services.user import create_new_user


class CustomModelViewSet(ModelViewSet):
    pagination_class = CustomPagination

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.all()


class HiveUserViewSet(CustomModelViewSet):
    serializer_class = HiveUserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
    def list(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
    
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_new_user(**serializer.validated_data)
        serialized_user = self.get_serializer(user)
        return Response(serialized_user.data, status=201)
