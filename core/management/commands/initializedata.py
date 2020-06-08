from django.core.management.base import BaseCommand

from api.initialization_api.initialize_api import initialize_api


class Command(BaseCommand):
    """
    Populates project with initial data.

    Example: $ python manage.py initializedata
    """
    help = 'Inserts initial data'

    def handle(self, *args, **options):
        """
        Running each declared function

        :param args: None
        :param options: None
        :return: None
        """

        self.stdout.write(self.style.SUCCESS('Starting populating data for API module'))
        initialize_api()

        self.stdout.write(
            self.style.SUCCESS(
                '>>>>>>>>>>>>>>>>>>>>>>>>> Successfully initialized all data <<<<<<<<<<<<<<<<<<<<<<<<<<'))
