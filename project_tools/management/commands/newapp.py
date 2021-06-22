from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Start a new django app.'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str)

    def handle(self, *args, **options):
        print(args)
        print(options)
