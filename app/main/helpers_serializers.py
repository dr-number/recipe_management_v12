from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers

from main.models import User
from app.help_logger import logger
from app.helpers import get_headers

def serializer_logger(request, attrs, errors):
    attrs.pop('password', None)
    attrs.pop('password2', None)

    user: User = request.user
    user_info = ''
    if not user.is_anonymous:
        user_info = (
            'User\n'
            f'is_active: {user.is_active}\n'
            f'id: {user.id}\n'
            f'email: {user.email}\n'
        )
    logger.error(
        f'\n{request.method} :: {request.build_absolute_uri()}\n'
        f'<b>headers:</b> {get_headers(request)}\n'
        f'\n{user_info}\n'
        f'\nattrs:\n{attrs}\n'
        f'errors:\n{errors}\n'
    )

def validate_unexpected_fields():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            request = self.context['request']
            attrs = func(self, *args, **kwargs)
            expected_fields = set(self.fields.keys())
            received_fields = set(self.initial_data.keys())
            unexpected_fields = received_fields - expected_fields

            if unexpected_fields:
                error = f'Unexpected fields: {", ".join(unexpected_fields)}'
                serializer_logger(request=request, attrs=attrs, errors=error)
                raise serializers.ValidationError({
                    'unexpected_fields': error
                })
            return attrs
        return wrapper
    return decorator

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except ValidationError:
        pass

    return False