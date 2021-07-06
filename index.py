# -*- coding: utf-8 -*-
import sys
import os

# load local django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site-packages"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "django_bootstrap"))

from django_bootstrap.wsgi import application

import logging


# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
def initializer(context):
    logger = logging.getLogger()
    logger.info('initializing')


def handler(environ, start_response):
    return application(environ, start_response)
