import hashlib
import logging
import uuid

from django.views import View
from marshmallow import fields, validate, Schema

from django.core.cache import cache

from shared.auth.authentication import BaseAuthentication, AuthenticationFailed
from shared.response import GenericJsonResponse
from shared.view_decorators import json_request

logger = logging.getLogger(__name__)


class UsernameUserStoreBase:
    """
    The base class for username user store.
    """

    def get_user_by_username(self, username):
        raise NotImplementedError('Inherit MobileAuthLoginViewBase and implement get_user_by_mobile.')


class UsernamePasswordRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginView(View):
    ERROR_USERNAME_PASSWORD = GenericJsonResponse(code=1, message='用户名或密码不正确')

    @json_request(request_schema_class=UsernamePasswordRequestSchema)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = self.get_user_by_username(username)
        if not user:
            return self.ERROR_USERNAME_PASSWORD
        if not hashlib.md5(password.encode(encoding='utf8')).hexdigest() == user.password:
            return self.ERROR_USERNAME_PASSWORD

        token = self.cache_token(username)
        return GenericJsonResponse(data=dict(token=token))

    @staticmethod
    def cache_token(uid, expiration_time=30 * 24 * 60 * 60):
        """ 缓存user, 生成token """
        token = uuid.uuid4().hex
        cache.set('user_token_' + token, uid, expiration_time)
        logger.info(f"cached user uid: {uid}, "
                    f"expiration time: {expiration_time}s")
        return token
