class BaseAuthentication:
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        raise NotImplementedError(".authenticate() must be overridden.")


class AuthenticationFailed(Exception):
    pass
