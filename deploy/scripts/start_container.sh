docker rm -f django_bootstrap-redis \
&& docker run -d --name django_bootstrap-redis -p 6379:6379 redis:3 --requirepass "rkrGtsuBsdiok"

docker rm -f django_bootstrap \
&& docker run \
--name django_bootstrap \
--sysctl net.core.somaxconn=10000 \
-v /var/log/django_bootstrap:/var/logs/django_bootstrap \
-v /opt/django_bootstrap:/opt/django_bootstrap \
-v /root/data/django_bootstrap_uploads:/data/uploads \
--link django_bootstrap-redis:django_bootstrap-redis \
--env DYNACONF_DEBUG="True" \
--env DYNACONF_IN_ALIYUN_FC="True" \
--env DYNACONF_MYSQL_HOST="0.0.0.0" \
--env DYNACONF_MYSQL_PORT="3306" \
--env DYNACONF_MYSQL_NAME="django_bootstrap" \
--env DYNACONF_MYSQL_USER="root" \
--env DYNACONF_MYSQL_PASSWORD="123456" \
--env DYNACONF_MYSQL_NAME_TEST="django_bootstrap_test" \
--env DYNACONF_REDIS_ADDRESS=":123456@0.0.0.0:6379" \
--env DYNACONF_ALI_SMS_APP_KEY="xxx" \
--env DYNACONF_ALI_SMS_SECRET_KEY="xxx" \
--env DYNACONF_ALI_SMS_SIGN_NAME="xxx" \
--env DYNACONF_ALI_SMS_TEMPLATE_CODE="xxx" \
--env DYNACONF_LOG_DIR="/var/logs" \
--env DYNACONF_WX_MINI_APPID="xxxx" \
--env DYNACONF_WX_MINI_SECRET="xxxx" \
-p 8080:8080 \
-d django_bootstrap:v1_0
