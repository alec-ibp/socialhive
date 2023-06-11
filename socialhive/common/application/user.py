from django.contrib.auth.hashers import make_password

from socialhive.common.dtos import UserRegisterDTO
from socialhive.common.models import HiveUser
from socialhive.common.exceptions import DataValidationError
from socialhive.common.infrastructure.repository.interfaces import UserServiceAbstractRepository


class UserServiceManager:
    def __init__(self, repository: UserServiceAbstractRepository) -> None:
        self.repository = repository

    def create_user(self, user_dto: UserRegisterDTO) -> HiveUser:
        user_dto.password = make_password(user_dto.password)
        return self.repository.create_user(user_dto)

    def change_password(self, current_user: HiveUser, old_password: str, new_password: str, new_password_confirmation: str) -> None:
        coincidences: int = 0
        password_length: int = min(len(new_password), len(old_password))
        for i in range(password_length):
            if old_password[i].lower() == new_password[i].lower():
                coincidences += 1

        if not current_user.check_password(old_password):
            raise DataValidationError("Old password is incorrect.")
        if new_password != new_password_confirmation:
            raise DataValidationError("New password and confirmation don't match.")
        if old_password.lower() == new_password.lower():
            raise DataValidationError("New password can't be the same as the old one.")
        if coincidences >= password_length // 2 or old_password in new_password or new_password in old_password:
            raise DataValidationError("New password can't be too similar to the old one.")

        self.repository.update_password(current_user, new_password)
