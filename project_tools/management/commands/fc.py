import logging
import shutil
import site
import time
from pathlib import Path

from django.core.management.base import BaseCommand

from tempfile import TemporaryDirectory

from django_bootstrap.settings import BASE_DIR

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Alibaba cloud function computing commands '

    def add_arguments(self, parser):
        parser.add_argument('--deploy', action="store_true")

    def handle(self, *args, **options):
        if options.get("deploy", False):
            self.deploy()

    @staticmethod
    def deploy():
        with TemporaryDirectory() as dirname:
            app_dir = Path(dirname) / Path('django_bootstrap_' + str(int(time.time())))
            print('App dir: ' + str(app_dir))
            print('Creating the app zip file......')
            shutil.copytree(BASE_DIR, app_dir)

            libs = site.getsitepackages()
            for lib in libs:
                shutil.copytree(lib, app_dir, dirs_exist_ok=True)

            shutil.make_archive(str(app_dir), 'zip', str(app_dir))
            shutil.copyfile(str(app_dir) + ".zip", '/Users/xiewangyi/Downloads/111.zip')
        # Use the directory
        # Directory and all contents destroyed
