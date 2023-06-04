from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from simple_history.models import HistoricalRecords


class CustomHiveUserManager(BaseUserManager):
    def _create_user(self, email: str, username: str, password:str, **kwargs) -> 'HiveUser':
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('username is required')

        user = self.model(
            self.normalize_email(email),
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, username: str, password: str, **kwargs) -> 'HiveUser':
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email=email, username=username, password=password, **kwargs)
    
    def create_super_user(self, email: str, password: str, **kwargs) -> 'HiveUser':
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        user = self._create_user(email=email, password=password, **kwargs)
        user.save(using=self._db)
        return user


class HiveUser(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.IntegerChoices):
        ADMIN = 1
        USER = 2

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=265)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.IntegerField(choices=UserRole.choices, default=UserRole.USER)

    history = HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomHiveUserManager()

    def __str__(self):
        return self.email
