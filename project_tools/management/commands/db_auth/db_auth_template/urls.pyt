from django.urls import path

from .mobile.support_mobile import MobileAuthSendSMSView, MobileAuthLoginView
from .user_and_pass.support_username_password import UsernameLoginView
from .wechat.support_wechat_mini import WechatMiniAuthLoginView

urlpatterns = [
    path('wechat_mini_auth/login', WechatMiniAuthLoginView.as_view()),
    path('mobile_auth/send_sms', MobileAuthSendSMSView.as_view()),
    path('mobile_auth/login', MobileAuthLoginView.as_view()),
    path('wechat_mini_auth/login', UsernameLoginView.as_view()),
]
