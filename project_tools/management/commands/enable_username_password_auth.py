from django.core.management.base import BaseCommand

from django_bootstrap.settings import BASE_DIR
from project_tools.file_content_util import insert_text_after


class Command(BaseCommand):
    help = 'Enable username password db_auth in this app.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        new_app_name = options.get('app_name').lower()

        # Add url patterns
        urls_file = BASE_DIR / new_app_name / 'urls.py'
        file_content = urls_file.read_text(encoding='utf-8')

        if file_content.find(
                "from shared.db_auth.user_and_pass.support_username_password import LoginView") >= 0:
            return

        file_content = insert_text_after(
            file_content,
            'from django.urls import path',
            '\nfrom shared.db_auth.demo.username_user_store import MobileUserStoreDemo'
            '\nfrom shared.db_auth.user_and_pass.support_username_password import LoginView'
        )
        file_content = insert_text_after(
            file_content,
            'urlpatterns = [',
            "\n    path('username_password_auth/login', type('UsernameLoginView', (LoginView, MobileUserStoreDemo), "
            "dict()).as_view()),"
        )
        urls_file.write_text(file_content)
