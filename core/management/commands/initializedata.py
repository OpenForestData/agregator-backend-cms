from django.core.management.base import BaseCommand

from api.initialization_api.initialize_api import create_static_basic_filters_fields, create_basic_templates_data, \
    create_basic_articles_and_keyword, create_add_menu_links


class Command(BaseCommand):
    """
    Populates project with initial data.

    Example: $ python manage.py initializedata
    """
    help = 'Inserts initial data'

    def handle(self, *args, **options):
        """
        Running each declared function to initialize data in agregator backend cms

        :param args: None
        :param options: None
        :return: None
        """

        self.stdout.write(self.style.SUCCESS('Starting populating data for API module'))
        self.stdout.write(self.style.SUCCESS('...Starting initializing basic filters fields'))
        create_static_basic_filters_fields()
        self.stdout.write(self.style.SUCCESS('Finished initializing basic filters fields...'))
        self.stdout.write(self.style.SUCCESS('...Starting initializing basic cms structure '))
        create_basic_templates_data()
        create_add_menu_links()
        self.stdout.write(self.style.SUCCESS('Finished initializing basic cms structure ...'))
        self.stdout.write(self.style.SUCCESS('...Starting initializing basic news data '))
        create_basic_articles_and_keyword()
        self.stdout.write(self.style.SUCCESS('Finished initializing basic news data ...'))
        self.stdout.write(
            self.style.SUCCESS(
                '>>>>>>>>>>>>>>>>>>>>>>>>> Successfully initialized all data <<<<<<<<<<<<<<<<<<<<<<<<<<'))
