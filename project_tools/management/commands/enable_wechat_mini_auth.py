from pathlib import Path

from django.core.management.base import BaseCommand

from django_bootstrap.settings import BASE_DIR
from project_tools.file_content_util import insert_text_after


class Command(BaseCommand):
    help = 'Enable wechat mini auth in this app.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        new_app_name = options.get('app_name').lower()

        # Add url patterns
        urls_file = BASE_DIR / new_app_name / 'urls.py'
        file_content = urls_file.read_text(encoding='utf-8')

        if file_content.find("from shared.auth.wechat.support_wechat_mini import WechatMiniAuthLoginView") >= 0:
            return

        file_content = insert_text_after(
            file_content,
            'from django.urls import path',
            '\nfrom shared.auth.demo.union_id_user_store import UnionIdUserStore'
            '\nfrom shared.auth.wechat.support_wechat_mini import WechatMiniAuthLoginView'
        )
        file_content = insert_text_after(
            file_content,
            'urlpatterns = [',
            "\n    path('wechat_mini_auth/login', type('WechatMiniLoginView', "
            "(WechatMiniAuthLoginView, UnionIdUserStore), "
            "dict()).as_view()),"
        )
        urls_file.write_text(file_content)
