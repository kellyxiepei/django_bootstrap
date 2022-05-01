from shared.auth.user_and_pass.support_username_password import UsernameUserStoreBase


class DemoUsernameUser:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


class MobileUserStoreDemo(UsernameUserStoreBase):
    def get_user_by_username(self, username):
        return DemoUsernameUser(username, 'e10adc3949ba59abbe56e057f20f883e')
