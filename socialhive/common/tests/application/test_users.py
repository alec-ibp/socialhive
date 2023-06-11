import pytest

from socialhive.common.application.user import UserServiceManager
from socialhive.common.models import HiveUser
from socialhive.common.tests.factories import UserDTOFactory


class TestUserApplicationManager:
    @pytest.fixture(autouse=True)
    def setup_method(self, fake_repository):
        self.user_manager = UserServiceManager(repository=fake_repository)
        return self.user_manager

    def test_create_user(self):
        user_dto = UserDTOFactory()
        user_password: str = user_dto.password
        created_user = self.user_manager.create_user(user_dto=user_dto)
        assert isinstance(created_user, HiveUser)
        assert created_user.username == user_dto.username
        assert created_user.email == user_dto.email
        assert created_user.password == user_dto.password
        assert created_user.check_password(user_password)
