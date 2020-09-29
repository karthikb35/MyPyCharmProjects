class AuthException(Exception):
    def __init__(self, username, user = None):
        super().__init__(username,user)
        self.username = username
        self.user = user

class UsernameAlreadyExisits(AuthException):
    pass


class PasswordTooShort(AuthException):
    pass

