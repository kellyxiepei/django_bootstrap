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


