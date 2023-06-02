from rest_framework.serializers import ModelSerializer

from socialhive.common.models import HiveUser


class HiveUserSerializer(ModelSerializer):
    class Meta:
        model = HiveUser
        fields = (
            "username",
            "email",
            "password",
            "is_active",
        )

    def to_representation(self, instance: HiveUser) -> dict:
        return {
            "username": instance.username,
            "email": instance.email,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
        }
    