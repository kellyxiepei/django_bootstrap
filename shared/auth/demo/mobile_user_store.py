from shared.auth.mobile.support_mobile import MobileUserStoreBase


class DemoMobileUser():
    def __init__(self, mobile):
        self._mobile = mobile


class MobileUserStoreDemo(MobileUserStoreBase):
    def get_user_by_mobile(self, mobile):
        return DemoMobileUser(mobile)
