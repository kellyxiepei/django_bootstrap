import logging
import random
import time
import uuid

from django.core.cache import cache
from django.views import View

from shared.auth.authentication import AuthenticationFailed, BaseAuthentication
from shared.auth.mobile.support_mobile_ali_sms_util import send_sms, SendSmsTooOften, SmsServiceIssue, SendSmsFailed
from shared.redis_utils import RedisUtil
from shared.response import GenericJsonResponse
from shared.view_decorators import json_request
from marshmallow import Schema, fields, validate

logger = logging.getLogger(__name__)


class MobileAuthSendSMSRequestSchema(Schema):
    mobile = fields.Str(required=True,
                        validate=validate.Regexp(regex=r"^(?=\d{11}$)^1[3456789]\d{9}$", error='Invalid mobile'))


class MobileAuthSendSMSView(View):
    ERROR_TOO_OFTEN = GenericJsonResponse(code=1, message='发送短信过于频繁, 请间隔60s重试')
    ERROR_SMS_SERVICE_ERROR = GenericJsonResponse(code=2, message='短信服务异常')
    ERROR_SMS_ERROR = GenericJsonResponse(code=3, message='短信发送失败')

    @json_request(request_schema_class=MobileAuthSendSMSRequestSchema)
    def post(self, request):
        app_name = request.resolver_match.app_name

        mobile = request.data.get('mobile')

        if not self._verify_last_send_time(mobile):
            return self.ERROR_TOO_OFTEN

        verify_code = self._gen_verify_code()

        try:
            send_sms(mobile, verify_code)
        except SendSmsTooOften:
            return self.ERROR_TOO_OFTEN
        except SmsServiceIssue:
            return self.ERROR_SMS_SERVICE_ERROR
        except SendSmsFailed:
            return self.ERROR_SMS_ERROR

        self._record_last_send_code_and_time(verify_code, mobile, app_name)

        return GenericJsonResponse()

    @staticmethod
    def _gen_verify_code():
        # 生成短信验证码
        verify_code = random.randint(0, 999999)
        verify_code = format(verify_code, '>06d')
        return verify_code

    @staticmethod
    def _record_last_send_code_and_time(verify_code, mobile, app_name):
        # 记录该phone最新发短信的时间
        send_time = time.time()
        RedisUtil.set_key(key=f'sms_last_send_time_{mobile}',
                          value=send_time, ex_time=10 * 60)

        RedisUtil.set_key(key=f'{app_name}_sms_login_code_{mobile}',
                          value=verify_code, ex_time=10 * 60)

    @staticmethod
    def _verify_last_send_time(mobile):
        # 验证该union_id上次发送短信时间
        now = time.time()
        last_time = RedisUtil.get_key(
            key=f'sms_last_send_time_{mobile}') or "0.0"
        if now - float(last_time) > 60:
            return True
        return False


class MobileAuthLoginRequestSchema(Schema):
    mobile = fields.Str(required=True,
                        validate=validate.Regexp(regex=r"^(?=\d{11}$)^1[3456789]\d{9}$", error='手机号码不正确'))
    code = fields.Str(required=True,
                      validate=validate.Regexp(regex=r'\d{6}', error='验证码不正确'))


class MobileUserStoreBase:
    """
    The base class for mobile user store.
    """

    def get_user_by_mobile(self, mobile):
        raise NotImplementedError('Inherit MobileAuthLoginViewBase and implement get_user_by_mobile.')


class MobileAuthLoginView(View):
    ERROR_INVALID_CODE = GenericJsonResponse(code=1, message="验证码不正确")
    ERROR_USER_NOT_EXIST = GenericJsonResponse(code=2, message="用户不存在")

    @json_request(request_schema_class=MobileAuthLoginRequestSchema)
    def post(self, request):
        app_name = request.resolver_match.app_name
        mobile = request.data.get('mobile')
        code = request.data.get('code')

        if not self.verify_code(app_name, code, mobile):
            return self.ERROR_INVALID_CODE

        user = self.get_user_by_mobile(mobile)
        if not user:
            return self.ERROR_USER_NOT_EXIST

        token = self.cache_token(mobile)
        return GenericJsonResponse(data=dict(token=token))

    @staticmethod
    def verify_code(app_name, code, mobile):
        logger.info(f'start verify sms code, mobile: {mobile}, code: {code}')
        key = f'{app_name}_sms_login_code_{mobile}'
        logger.debug(f'sms key: {key}')
        code = RedisUtil.get_key(key=key)
        logger.debug(f'get sms code from redis: {code}')
        if code and code == code:
            RedisUtil.delete_key(key)
            logger.info('verify ok')
            return True
        logger.info('verify bad')
        return False

    @staticmethod
    def cache_token(mobile, expiration_time=30 * 24 * 60 * 60):
        """ 缓存user, 生成token """
        token = uuid.uuid4().hex
        cache.set('user_token_' + token, mobile, expiration_time)
        logger.info(f"cached user uid: {mobile}, "
                    f"expiration time: {expiration_time}s")
        return token


class MobileAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            raise AuthenticationFailed('您未登陆')
        mobile = cache.get('user_token_' + token)
        if not mobile:
            raise AuthenticationFailed('您未登陆')
        user = self.get_user_by_mobile(mobile)
        if not user:
            raise AuthenticationFailed('您未登录')

        return user
