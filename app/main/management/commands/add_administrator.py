import logging
import sys
import random

from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand
from main.models import User
from main.helpers.helpers_admin import generate_password
from app.helpers import is_valid_email


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

""" Clear all data and seed db """
MODE_REFRESH = 'refresh'

""" Clear all data and do not seed any object """
MODE_CLEAR = 'clear'

def get_or_create_default_admin():
    permissions = Permission.objects.filter(
        codename__in=[
            'add_customuser', 
            'view_customuser', 
            'view_feedback', 
            'add_strategy',
            'view_strategy',
            'view_user',
            'view_order',
            'view_orderpaymentinfo',
            'view_tariff',
        ]
    )
    admin_group, created = Group.objects.get_or_create(name='default_admin')
    admin_group.permissions.set(permissions)
    return admin_group

def get_or_create_admin_only_custom_documents():
    permissions = Permission.objects.filter(
        codename__in=[
            'view_customdocument',
            'add_customdocument',
            'change_customdocument',
            'view_user'
        ]
    )
    admin_group, created = Group.objects.get_or_create(name='admin_only_custom_documents')
    admin_group.permissions.set(permissions)
    return admin_group

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode", default=MODE_REFRESH)

    def handle(self, *args, **options):
        self.stdout.write('adding administrator...')
        email = input("Enter the administrator's email address: ").lower()

        if not email:
            self.stdout.write(self.style.ERROR('Email must not be empty'))
            return

        if not is_valid_email(email=email):
            self.stdout.write(self.style.ERROR('Invalid email'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'A user with email {email} already exists.'))
            return

        self.stdout.write(self.style.WARNING('[1] - default admin'))
        self.stdout.write(self.style.WARNING('[2] - admin only custom documents'))
        role = input("select role (input number): ").lower()

        if role not in ['1', '2']:
            self.stdout.write(self.style.ERROR(f'unknown role'))
            return


        len_password = 54 + random.randint(5, 20)
        _password = generate_password(
            length=len_password, 
            use_letters=True, 
            use_digits=True, 
            use_punctuation=True
        )

        admin_user = User.objects.create_user(
            email=email,
            username=email,
            password=_password,
            first_name=email,
            last_name=email,
            is_active=True,
            is_staff=True,
            is_superuser=False
        )
        if not role or role == '1':
            admin_user.groups.add(get_or_create_default_admin())
        elif role == '2':
            admin_user.groups.add(get_or_create_admin_only_custom_documents())

        self.stdout.write('your email:\n\n')
        self.stdout.write(self.style.SUCCESS(email))
        self.stdout.write('your password:\n\n')
        self.stdout.write(self.style.SUCCESS(_password))
        self.stdout.write('\ndone.')
