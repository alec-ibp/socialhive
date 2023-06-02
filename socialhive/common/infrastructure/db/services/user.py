from django.contrib.auth.hashers import make_password

from socialhive.common.models import HiveUser


def create_new_user(username: str, email: str, password: str, **extra_data: dict) -> HiveUser:
    hashed_password = make_password(password)
    user = HiveUser.objects.create(
        username=username,
        email=email,
        password=hashed_password
    )
    return user
