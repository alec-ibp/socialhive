from rest_framework import serializers 

from socialhive.common.models import HiveUser


class HiveUserSerializer(serializers.ModelSerializer):
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
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "is_active": instance.is_active,
            "is_staff": instance.is_staff,
            "role": instance.role,
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)
