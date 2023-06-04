from socialhive.common.models import HiveUser
from socialhive.common.dtos import UserRegisterDTO
from ..interfaces import UserServiceAbstractRepository


class UserServiceRespository(UserServiceAbstractRepository):
    def create_user(self, user_dto: UserRegisterDTO) -> HiveUser:
        return HiveUser.objects.create(
            username=user_dto.username,
            email=user_dto.email,
            password=user_dto.password
        )

    def get_user_by_id(self, user_id: int) -> HiveUser:
        pass

    def get_user_by_email(self, email: str) -> HiveUser:
        pass

    def update_user(self, user: HiveUser) -> HiveUser:
        pass

    def delete_user(self, user_id: int) -> None:
        pass

    def update_password(self, user: HiveUser, new_password: str) -> None:
        user.set_password(new_password)
        user.save()
