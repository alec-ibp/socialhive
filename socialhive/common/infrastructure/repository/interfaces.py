from abc import ABC, abstractmethod

from socialhive.common.models import HiveUser
from socialhive.common.dtos import UserRegisterDTO


class UserServiceAbstractRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserRegisterDTO) -> HiveUser:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> HiveUser:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> HiveUser:
        pass

    @abstractmethod
    def update_user(self, user: HiveUser) -> HiveUser:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def update_password(self, user: HiveUser, new_password: str) -> None:
        pass