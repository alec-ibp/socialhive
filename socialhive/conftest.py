import pytest
from rest_framework.test import APIClient

from socialhive.common.models import HiveUser
from socialhive.common.dtos import UserRegisterDTO
from socialhive.common.tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def get_session(user, api_client):
    api_client.force_authenticate(user=user)
    return api_client, user


class TestBase:
    @pytest.fixture(autouse=True)
    def setup(self, get_session):
        self.api_client, self.user = get_session
        return api_client, user


class FakeUserServiceRepository:
    def create_user(self, user_dto: UserRegisterDTO) -> HiveUser:
        return HiveUser(username=user_dto.username, email=user_dto.email, password=user_dto.password)

    def update_password(self, user: HiveUser, new_password: str) -> None:
        user.set_password(new_password)


@pytest.fixture
def fake_repository():
    return FakeUserServiceRepository()
