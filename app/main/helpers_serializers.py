from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import serializers

def validate_unexpected_fields():
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # request = self.context['request']
            attrs = func(self, *args, **kwargs)
            expected_fields = set(self.fields.keys())
            received_fields = set(self.initial_data.keys())
            unexpected_fields = received_fields - expected_fields

            if unexpected_fields:
                error = f'Unexpected fields: {", ".join(unexpected_fields)}'
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