import pytest

from django.contrib.auth.hashers import make_password

from socialhive.common.application.user import UserServiceManager
from socialhive.common.models import HiveUser
from socialhive.common.exceptions import DataValidationError
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

    @pytest.mark.parametrize(
        ["validation", "new_password", "new_password_confirmation"],
        [
            ("old_incorrect", "test_new_password", "test_new_password"),
            ("not_match", "test_new_password", "TEST_NEW_PASSWORD"),
            ("identical", "test_new_password", "test_new_password"),
            ("to similar", "test_new_password", "TEST_NEW_PASSWORD"),
        ],
    )
    def test_incorrect_new_password(self, validation: str, new_password: str, new_password_confirmation: str):
        current_password: str = make_password('current_password')
        current_user = HiveUser(
            username="test_user",
            email="test@test.com",
            password=current_password,
        )

        if validation == "old_incorrect":
            old_password: str = "wrong_current_password"
            new_password: str = "test_new_password"
            new_password_confirmation: str = "test_new_password"
            error_message: str = "Old password is incorrect."
        elif validation == "not_match":
            old_password: str = "current_password"
            new_password: str = "test_new_password"
            new_password_confirmation: str = "not_match_password"
            error_message: str = "New password and confirmation don't match."
        elif validation == "identical":
            old_password: str = "current_password"
            new_password: str = "current_password"
            new_password_confirmation: str = "current_password"
            error_message: str = "New password can't be the same as the old one."
        elif validation == "to similar":
            old_password: str = "current_password"
            new_password: str = "new_current_password"
            new_password_confirmation: str = "new_current_password"
            error_message: str = "New password can't be too similar to the old one."

        with pytest.raises(DataValidationError) as excinfo:
            self.user_manager.change_password(
                current_user=current_user,
                old_password=old_password,
                new_password=new_password,
                new_password_confirmation=new_password_confirmation,
            )
        assert error_message in str(excinfo.value)

    def test_success_change_password(self):
        current_password: str = make_password('current_password')
        current_user = HiveUser(
            username="test_user",
            email="test@test.com",
            password=current_password,
        )

        new_password: str = "test_new_password"
        new_password_confirmation: str = "test_new_password"

        self.user_manager.change_password(
            current_user=current_user,
            old_password="current_password",
            new_password=new_password,
            new_password_confirmation=new_password_confirmation,
        )
        assert current_user.check_password(new_password)
        assert not current_user.check_password("current_password")
