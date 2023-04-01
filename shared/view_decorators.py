import functools
import json

from marshmallow import ValidationError

from shared.auth.authentication import AuthenticationFailed
from shared.response import GenericJsonResponse


def json_request(request_schema_class=None):
    def deco(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            request.json = json.loads(request.body.decode(encoding='utf-8'))
            if request_schema_class is not None:
                schema = request_schema_class()
                try:
                    request.data = schema.load(request.json)
                except ValidationError as e:
                    return GenericJsonResponse(code=1, message="请求参数不合法", data=e.messages)
            return func(self, request, *args, **kwargs)

        return wrapper

    return deco


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

def exception_handlers():
    def deco(func):
        @functools.wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                return func(self, request, *args, **kwargs)
            except Exception as e:
                return GenericJsonResponse(code=2, message=str(e))
        return wrapper
    return deco
