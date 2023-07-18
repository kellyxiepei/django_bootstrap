import functools

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
