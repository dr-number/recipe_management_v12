from rest_framework import serializers

from main.helpers_serializers import validate_unexpected_fields, is_valid_email
from main.const import (
    KEY_USER_TYPES_CHOICES
)

class CreateAccountSerializer(serializers.Serializer):
    email = serializers.CharField(
        label='email', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=255
    )
    first_name = serializers.CharField(
        label='first_name', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=255
    )
    last_name = serializers.CharField(
        label='last_name', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=255
    )
    password = serializers.CharField(
        label='password', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=255
    )
    password2 = serializers.CharField(
        label='password2', 
        write_only=True, 
        required=True,
        allow_blank=False,
        max_length=255
    )
    type = serializers.ChoiceField(
        label='type', 
        write_only=True, 
        allow_blank=False,
        required=True,
        choices=KEY_USER_TYPES_CHOICES
    )

    @validate_unexpected_fields()
    def validate(self, attrs):
        errors = {}

        email = attrs['email']

        if not is_valid_email(email=email):
            errors['email'] = [
                'Некорректный адрес электронной почты'
            ]

        if attrs.get('password') != attrs.get('password2'):
            errors['password'] = ['Пароли не совпадают']
            errors['password2'] = ['Пароли не совпадают']

        return super().validate(attrs)
