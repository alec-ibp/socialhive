from django.urls import path

from socialhive.common.infrastructure.api.views import HiveUserViewSet, HiveUserRegisterView

urlpatterns = [
    path('users/register/', HiveUserRegisterView.as_view(), name="user-register"),
    path('users/me/', HiveUserViewSet.as_view({"get": "me"}), name="users-me"),
    path('users/<int:pk>/', HiveUserViewSet.as_view({"put": "update", "delete": "destroy"}), name="users-update"),
    path('users/change-password/', HiveUserViewSet.as_view({"post": "change_password"}), name="users-change-password"),
]
