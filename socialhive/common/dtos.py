class UserRegisterDTO:
    def __init__(self, username: str, email: str, password: str, **extra_data: dict):
        self.username = username
        self.email = email
        self.password = password
        self.extra_data = extra_data
