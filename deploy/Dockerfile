########################
# run the script to build:
# docker build -t "django_bootstrap:v1_0" -f ./deploy/Dockerfile .
########################
FROM python:3.9.2

MAINTAINER xiewangyi

##############
# set env
##############
# pip env
ENV PIP_NO_CACHE_DIR=off
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

#############
# apt install
#############
RUN apt-get update \
    && apt-get install -y tcl8.6-dev tk8.6-dev python-tk default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

################
# install pipenv
################
RUN pip install poetry


##############
# set env
##############
ENV DYNACONF_DEBUG=""
ENV DYNACONF_IN_ALIYUN_FC=""
ENV DYNACONF_MYSQL_HOST=""
ENV DYNACONF_MYSQL_PORT=""
ENV DYNACONF_MYSQL_NAME=""
ENV DYNACONF_MYSQL_USER=""
ENV DYNACONF_MYSQL_PASSWORD=""
ENV DYNACONF_MYSQL_NAME_TEST=""
ENV DYNACONF_REDIS_ADDRESS=""
ENV DYNACONF_ALI_SMS_APP_KEY=""
ENV DYNACONF_ALI_SMS_SECRET_KEY=""
ENV DYNACONF_ALI_SMS_SIGN_NAME=""
ENV DYNACONF_ALI_SMS_TEMPLATE_CODE=""
ENV DYNACONF_LOG_DIR=""
ENV DYNACONF_WX_MINI_APPID=""
ENV DYNACONF_WX_MINI_SECRET=""
ENV DYNACONF_UPLOAD_FILES_DIR=""


# mount the files
VOLUME ["/var/logs/django_bootstrap", "/opt/django_bootstrap", "/data/uploads"]

WORKDIR /opt/django_bootstrap

CMD pip install --upgrade poetry pip \
    && poetry export --without-hashes --dev -f requirements.txt -o requirements.txt \
    && pip install -r requirements.txt \
    && python manage.py migrate --noinput \
    && uwsgi deploy/uwsgi.ini

EXPOSE 8080
