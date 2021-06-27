from shared.auth.authentication import BaseAuthentication, AuthenticationFailed


class DemoUser:
    def __init__(self, username, role):
        self._username = username
        self._role = role


class DemoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', '')
        if token == 'xxxx123':
            return DemoUser('test_user', 1)
        else:
            raise AuthenticationFailed('您未登陆')
