from pathlib import Path

from django.core.management.base import BaseCommand

from distutils.dir_util import copy_tree
from distutils.file_util import move_file

from django_bootstrap.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Start a new django app with a pre-defined code structure.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        new_app_name = options.get('app_name').lower()
        new_app_name_pascal = ''.join(x.title() for x in new_app_name.split('_'))
        new_app_name_kebab = new_app_name.replace('_', '-')

        src_path = Path(__file__).parent / 'newapp' / 'new_app_template'
        target_path = BASE_DIR / new_app_name
        copy_tree(str(src_path), str(target_path))

        pyt_files = target_path.glob('**/*.pyt')
        for file in pyt_files:
            move_file(str(file), str(file)[:-1])

        all_files = target_path.glob('**/*.*')
        for file in all_files:
            file_content = file.read_text(encoding='utf-8')
            file_content = file_content.replace('##PascalAppName##', new_app_name_pascal)
            file_content = file_content.replace('##snake_app_name##', new_app_name)
            file.write_text(file_content, encoding='utf-8')

        # Add url patterns
        urls_file = BASE_DIR / 'django_bootstrap' / 'urls.py'
        file_content = urls_file.read_text(encoding='utf-8')
        insert_point = file_content.find('urlpatterns = [') + len('urlpatterns = [')
        new_file_content = file_content[:insert_point]
        new_file_content += f"\n    path('api/{new_app_name_kebab}/', " \
                            f"include(('{new_app_name}.urls', '{new_app_name}')), name='{new_app_name}'),"
        new_file_content += file_content[insert_point:]
        urls_file.write_text(new_file_content)

        # Add installed app
        settings_file = BASE_DIR / 'django_bootstrap' / 'settings.py'
        file_content = settings_file.read_text(encoding='utf-8')
        insert_point = file_content.find('INSTALLED_APPS = [') + len('INSTALLED_APPS = [')
        new_file_content = file_content[:insert_point]
        new_file_content += f"\n    '{new_app_name}.apps.{new_app_name_pascal}Config',"
        new_file_content += file_content[insert_point:]
        settings_file.write_text(new_file_content)
