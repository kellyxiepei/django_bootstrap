import functools

from django.core.cache import cache
from db_auth.models import User
from shared.response import GenericJsonResponse


class BaseAuthentication:
    """
    All authentication classes should extend BaseAuthentication.
    """

    """
    Should return authenticated user object, or raise AuthenticationFailed
    """

    def authenticate(self, request):
        raise NotImplementedError(".authenticate() must be overridden.")


class AuthenticationFailed(Exception):
    pass


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            raise AuthenticationFailed('您未登陆')
        user_id = cache.get('user_token_' + token)
        if not user_id:
            raise AuthenticationFailed('您未登陆')
        user = User.objects.get(id=user_id)
        if not user:
            raise AuthenticationFailed('您未登录')

        return user


def require_authentication(authenticator_class):
    def deco(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                authenticator = authenticator_class()
                request.user = authenticator.authenticate(request)
            except AuthenticationFailed as e:
                return GenericJsonResponse(code=2, message='您未登陆')
            return func(self, request, *args, **kwargs)

        return wrapper

    return deco
