import factory

from django.contrib.auth.hashers import make_password

from socialhive.common.models import HiveUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HiveUser

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = make_password(str("test_password"))
    is_active = True
    is_staff = False
    role = 2
