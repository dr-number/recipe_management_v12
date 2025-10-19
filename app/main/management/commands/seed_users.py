import logging
import os
import sys

from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand
from main.models import User
from django.core.management.base import BaseCommand, CommandError

from app.settings import DEBUG

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

""" Clear all data and seed db """
MODE_REFRESH = 'refresh'

""" Clear all data and do not seed any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode", default=MODE_REFRESH)

    def handle(self, *args, **options):
        if not DEBUG:
            raise CommandError('The "seed_users" command is disabled.')
            
        self.stdout.write('seeding data...')
        run_seed(options['mode'])
        self.stdout.write('done.')


# def clear_data():
#     """Deletes all the table data"""
#     models_to_clear = [User]
#     logger.info(f"Delete {', '.join([m.__name__ for m in models_to_clear])} instances")
#     for model in models_to_clear:
#         model.objects.all().delete()


def run_seed(mode):
    if not User.objects.filter(email=os.getenv('ADMIN_LOGIN', 'admin')).exists():
        admin_user = User.objects.create_user(
            email=os.getenv('ADMIN_LOGIN', 'admin'),
            username=os.getenv('ADMIN_LOGIN', 'admin'),
            password=os.getenv('ADMIN_PASSWORD', 'adm1npassw0rd'),
            first_name=os.getenv('ADMIN_LOGIN', 'admin'),
            last_name=os.getenv('ADMIN_LOGIN', 'admin'),
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

