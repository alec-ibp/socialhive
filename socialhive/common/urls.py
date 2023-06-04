from django.urls import path

from socialhive.common.infrastructure.api.views import HiveUserViewSet

urlpatterns = [
    path('users/', HiveUserViewSet.as_view({"get": "list", "post": "create"}), name="users-list"),
    path('users/change-password/', HiveUserViewSet.as_view({"post": "change_password"}), name="users-change-password"),
]
