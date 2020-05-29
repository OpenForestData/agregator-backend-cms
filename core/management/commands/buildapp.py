import os
import subprocess

from core.settings import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from core.settings import PROJECT_DIR

AVAILABLE_BUILD_PARAMETERS = ["settings"]


class Command(BaseCommand):
    """
    Building parametrized script:
    Takes as --profile parameter one of AVAILABLE_BUILD_PARAMETERS.
    Each parameter name require file in xcaliber/settings/parameter_file.py with import * from common file.

    Example: $ python manage.py buildapp --profile production
    """

    help = 'Builds an app based on given parameter, example: --profile production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--profile',
            dest='profile',
            required=True,
            help=f'Select building profile: {AVAILABLE_BUILD_PARAMETERS}',
        )

    def handle(self, *args, **options):
        """
        Running every build command and print status to user.

        :param args: None
        :param options: profile name as string
        :return: None
        """
        # Running pytest for all project's app
        profile = options['profile']

        if profile not in AVAILABLE_BUILD_PARAMETERS:
            self.stdout.write(self.style.ERROR('Invalid profile parameter. Theese are available parameters:'))
            for available_profile in AVAILABLE_BUILD_PARAMETERS:
                self.stdout.write(available_profile + ",\n")
            exit()

        # Check if settings are correct (are equal to building profile ex. test=test)
        with open(os.path.join(PROJECT_DIR, 'core/settings/__init__.py'), 'r+') as settings_file:
            settings_file_content = settings_file.read()

        # When profile mismatch change settings and terminate script with message to rerun script
        if profile + " " not in settings_file_content:
            with open(os.path.join(PROJECT_DIR, 'core/settings/__init__.py'), 'w') as settings_file:
                settings_file.write('from .%s import *' % profile)
                settings_file.truncate()
                # Inform user about changed configuration
                self.stdout.write(self.style.ERROR('Replaced database configuration, rerun script.'))
                exit(1)

        # When database is sqlite so we need to remove a file (db)
        if "sqlite" in settings.DATABASES['default']['NAME']:
            if os.path.exists(os.path.join(PROJECT_DIR, 'sqliteproject.db')):
                os.remove(os.path.join(PROJECT_DIR, 'sqliteproject.db'))
        # When database is connected normally run cleardatabase command
        else:
            call_command('cleardatabase')
        call_command('removemigrations')
        # collect static files - standard django command
        call_command('collectstatic', interactive=False)
        # make new migration files - standard django command
        call_command('makemigrations', interactive=False)
        #  populate db based on migration files
        call_command('migrate', interactive=False)

        self.stdout.write(self.style.SUCCESS('Creating default superuser.'))
        User.objects.create_superuser("admin", "admin@admin.pl", "admin")
        self.stdout.write(self.style.SUCCESS('Created user account: l: admin, pw: admin'))
        call_command('initializedata')
        self.stdout.write(self.style.SUCCESS('>>>>>>>>>>>>>>>>>>>>>>>>> Successful build <<<<<<<<<<<<<<<<<<<<<<<<<<'))
