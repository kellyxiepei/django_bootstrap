import json
import logging
import uuid

import requests
from django.core.cache import cache
from django.views import View

from dynaconf import settings

from db_auth.models import User
from shared.response import GenericJsonResponse
from shared.view_decorators import json_request
from marshmallow import Schema, fields

logger = logging.getLogger(__name__)


class WechatMiniAuthLoginRequestSchema(Schema):
    code = fields.Str(required=True)


class UnionIdUserStore:
    """
    The base class for union id user store.
    """

    def get_user_by_union_id(self, union_id, nickname, avatar):
        try:
            user = User.objects.get(credential='union_id_' + union_id)
            return user
        except User.DoesNotExist:
            user = User.objects.create(
                credential='union_id_' + union_id,
                nickname=nickname,
                avatar_url=avatar
            )
            return user


class WechatMiniAuthLoginView(View, UnionIdUserStore):
    ERROR_INVALID_CODE = GenericJsonResponse(code=1, message="code不正确")
    ERROR_USER_NOT_EXIST = GenericJsonResponse(code=2, message="用户不存在")

    @json_request(request_schema_class=WechatMiniAuthLoginRequestSchema)
    def post(self, request):
        code = request.data.get('code')

        wechat_user_info = self.verify_code(code)
        if not wechat_user_info:
            return self.ERROR_INVALID_CODE

        user = self.get_user_by_union_id(wechat_user_info['union_id'])
        if not user:
            return self.ERROR_USER_NOT_EXIST

        token = self.cache_token(user.id)
        return GenericJsonResponse(data=dict(token=token))

    @staticmethod
    def verify_code(code):
        resp = requests.get(
            f'https://api.weixin.qq.com/sns/jscode2session?appid={settings.WX_MINI_APPID}&secret={settings.WX_MINI_SECRET}&js_code={code}&grant_type=authorization_code')

        resp_json = resp.json()
        if resp_json['errcode'] != 0:
            logger.warning(f'wx mini login error:{resp_json}')
            return None

        logger.info('verify ok')
        return dict(
            unionid=resp_json['unionid'],
            session_key=resp_json['session_key'],
            openid=resp_json['openid']
        )

    @staticmethod
    def cache_token(wechat_user_info, expiration_time=30 * 24 * 60 * 60):
        """ 缓存user, 生成token """
        token = uuid.uuid4().hex
        cache.set('user_token_' + token, json.dumps(wechat_user_info), expiration_time)
        logger.info(f"cached user union_id: {json.dumps(wechat_user_info)}, "
                    f"expiration time: {expiration_time}s")
        return token
