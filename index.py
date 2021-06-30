# -*- coding: utf-8 -*-
import sys
import os

# load local django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site-packages"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "django_bootstrap"))

from urllib.parse import urlparse
from django_bootstrap.wsgi import application
from django.conf import settings

import logging

base_path = None


# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
def initializer(context):
    logger = logging.getLogger()
    logger.info('initializing')


def handler(environ, start_response):
    # 如果没有使用自定义域名
    if environ['fc.request_uri'].startswith("/2016-08-15/proxy"):
        request_uri = environ['fc.request_uri']
        parsed_tuple = urlparse(request_uri)
        li = parsed_tuple.path.split('/')
        global base_path
        if not base_path:
            base_path = "/".join(li[0:5])
            settings.STATIC_URL = base_path + settings.STATIC_FC_URL

        context = environ['fc.context']
        environ['HTTP_HOST'] = '{}.{}.fc.aliyuncs.com'.format(context.account_id, context.region)
        environ['SCRIPT_NAME'] = base_path + '/'
        environ['IN_ALIYUN_FC'] = 'True'

    return application(environ, start_response)
