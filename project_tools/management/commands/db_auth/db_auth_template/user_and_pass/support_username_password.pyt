import hashlib
import logging
import uuid

from django.views import View
from marshmallow import fields, validate, Schema

from django.core.cache import cache

from ..authentication import BaseAuthentication, AuthenticationFailed

from db_auth.models import User
from shared.response import GenericJsonResponse
from shared.view_decorators import json_request

logger = logging.getLogger(__name__)


class UsernameUserStore:
    """
    The base class for username user store.
    """

    def get_user_by_username(self, username):
        try:
            user = User.objects.get(credential='username_' + username)
        except User.DoesNotExist:
            return None
        return user


class UsernamePasswordRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UsernameLoginView(View, UsernameUserStore):
    ERROR_USERNAME_PASSWORD = GenericJsonResponse(code=1, message='用户名或密码不正确')

    @json_request(request_schema_class=UsernamePasswordRequestSchema)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = self.get_user_by_username(username)
        if not user:
            return self.ERROR_USERNAME_PASSWORD
        if not hashlib.md5(password.encode(encoding='utf8')).hexdigest() == user.secret:
            return self.ERROR_USERNAME_PASSWORD

        token = self.cache_token(username)
        return GenericJsonResponse(data=dict(token=token))

    @staticmethod
    def cache_token(username, expiration_time=30 * 24 * 60 * 60):
        """ 缓存user, 生成token """
        token = uuid.uuid4().hex
        cache.set('user_token_' + token, username, expiration_time)
        logger.info(f"cached user username: {username}, "
                    f"expiration time: {expiration_time}s")
        return token


class UsernamePasswordAuthentication(BaseAuthentication, UsernameUserStore):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            raise AuthenticationFailed('您未登陆')
        username = cache.get('user_token_' + token)
        if not username:
            raise AuthenticationFailed('您未登陆')
        user = self.get_user_by_username(username)
        if not user:
            raise AuthenticationFailed('您未登录')

        return user
