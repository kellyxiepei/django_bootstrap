from distutils.dir_util import copy_tree
from distutils.file_util import move_file, copy_file
from pathlib import Path

from django.core.management.base import BaseCommand

from django_bootstrap.settings import BASE_DIR
from project_tools.file_content_util import insert_text_after


class Command(BaseCommand):
    help = 'Enable mobile db_auth in this app.'

    def add_arguments(self, parser):
        parser.add_argument('auth_type', type=str)

    def init_db_auth_app(self):
        src_path = Path(__file__).parent / 'db_auth' / 'db_auth_template'
        target_path = BASE_DIR / 'db_auth'
        if target_path.exists():
            return
        else:
            target_path.mkdir(parents=True, exist_ok=True)

        copy_file(str(src_path / '__init__.pyt'), str(target_path / '__init__.pyt'))
        copy_file(str(src_path / 'apps.pyt'), str(target_path / 'apps.pyt'))
        copy_file(str(src_path / 'authentication.pyt'), str(target_path / 'authentication.pyt'))
        copy_file(str(src_path / 'models.pyt'), str(target_path / 'models.pyt'))
        copy_file(str(src_path / 'urls.pyt'), str(target_path / 'urls.pyt'))

        copy_tree(str(src_path / 'migrations'), str(target_path / 'migrations'))

        pyt_files = target_path.glob('**/*.pyt')
        for file in pyt_files:
            move_file(str(file), str(file)[:-1])

        # Add url patterns
        urls_file = BASE_DIR / 'django_bootstrap' / 'urls.py'
        file_content = urls_file.read_text(encoding='utf-8')
        file_content = insert_text_after(
            file_content,
            'urlpatterns = [',
            f"\n    path('api/auth/', include(('db_auth.urls', 'db_auth')), name='db_auth'),"
        )
        urls_file.write_text(file_content)

        # Add installed app
        settings_file = BASE_DIR / 'django_bootstrap' / 'settings.py'
        file_content = settings_file.read_text(encoding='utf-8')
        file_content = insert_text_after(
            file_content,
            'INSTALLED_APPS = [',
            f"\n    'db_auth.apps.DbAuthConfig',"
        )

        settings_file.write_text(file_content)

    def handle(self, *args, **options):
        src_path = Path(__file__).parent / 'db_auth' / 'db_auth_template'
        target_path = BASE_DIR / 'db_auth'

        self.init_db_auth_app()

        auth_type = options.get('auth_type').lower()

        if auth_type == 'mobile':
            dir_name = 'mobile'
            import_statement = 'from .mobile.support_mobile import MobileAuthSendSMSView, MobileAuthLoginView'
            url_pattern = "path('mobile_auth/send_sms', MobileAuthSendSMSView.as_view()), \n" \
                          "    path('mobile_auth/login', MobileAuthLoginView.as_view()),"

        elif auth_type == 'user_and_pass':
            dir_name = 'user_and_pass'
            import_statement = 'from .user_and_pass.support_username_password import UsernameLoginView'
            url_pattern = "path('username_password_auth/login', UsernameLoginView.as_view()),"
        elif auth_type == 'wechat_mini':
            dir_name = 'wechat_mini'
            import_statement = 'from .wechat_mini.support_wechat_mini import WechatMiniAuthLoginView'
            url_pattern = " path('wechat_mini_auth/login', WechatMiniAuthLoginView.as_view()),"
        else:
            raise Exception(f'Unknown auth type: {auth_type}')

        urls_file = BASE_DIR / 'db_auth' / 'urls.py'
        file_content = urls_file.read_text(encoding='utf-8')
        if file_content.find(import_statement) >= 0:
            return

        file_content = insert_text_after(
            file_content,
            'from django.urls import path',
            f"\n{import_statement}"
        )
        file_content = insert_text_after(
            file_content,
            'urlpatterns = [',
            f"\n    {url_pattern}"
        )
        urls_file.write_text(file_content)

        copy_tree(str(src_path / dir_name), str(target_path / dir_name))
        pyt_files = target_path.glob('**/*.pyt')
        for file in pyt_files:
            move_file(str(file), str(file)[:-1])
