import json
import logging

from dynaconf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class SendSmsFailed(Exception):
    pass


class SendSmsTooOften(Exception):
    pass


class SmsServiceIssue(Exception):
    pass


too_often_error_codes = (
    'VALVE:M_MC',
    'VALVE:H_MC',
    'VALVE:D_MC')

service_issue_codes = (
    'Amount.NotEnough',
    'OutOfService',
    'DayLimitControl',
    'MonthLimitControl',
    'isv.BUSINESS_LIMIT_CONTROL',
    'isv.OUT_OF_SERVICE',
    'isv.AMOUNT_NOT_ENOUGH'
)

logger = logging.getLogger(__name__)

AK = settings.ALI_SMS_APP_KEY
SK = settings.ALI_SMS_SECRET_KEY
SIGN = settings.ALI_SMS_SIGN_NAME
TEMPLATE_CODE = settings.ALI_SMS_TEMPLATE_CODE

client = AcsClient(AK, SK, 'cn-hangzhou')


def check_resp(resp: dict):
    code = resp.get('Code', 'nothing')

    if code != 'OK':
        if code in too_often_error_codes:
            logger.warning(f'send sms too often: {code}')
            raise SendSmsTooOften(str(resp))
        elif code in service_issue_codes:
            logger.critical(f'send sms service issue: {code}')
            raise SmsServiceIssue(str(resp))
        else:
            logger.error(f'send sms issue: {code}')
            raise SendSmsFailed(str(resp))


def send_sms(phone: str, code: str):
    logger.info(f'send ali sms, phone: {phone}, code: {code}')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', SIGN)
    request.add_query_param('TemplateCode', TEMPLATE_CODE)
    request.add_query_param('TemplateParam', json.dumps({"code": code}))

    try:
        resp_json = json.loads(client.do_action_with_exception(request))
        logger.info(f'ali sms send done:\n{resp_json}')
    except Exception as e:
        logger.exception(e)
        raise SendSmsFailed(str(e))

    check_resp(resp_json)
