from django.contrib.auth.hashers import make_password

from socialhive.common.dtos import UserRegisterDTO
from socialhive.common.models import HiveUser
from socialhive.common.infrastructure.repository.interfaces import UserServiceAbstractRepository


class UserServiceManager:
    def __init__(self, repository: UserServiceAbstractRepository) -> None:
        self.repository = repository

    def create_user(self, user_dto: UserRegisterDTO) -> HiveUser:
        user_dto.password = make_password(user_dto.password)
        return self.repository.create_user(user_dto)
    
    def change_password(self, current_user: HiveUser, new_password: str) -> None:
        self.repository.update_password(current_user, new_password)
