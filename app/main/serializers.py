from rest_framework import serializers

from main.helpers_serializers import validate_unexpected_fields, is_valid_email, serializer_logger
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
        request = self.context['request']
        email = attrs['email']

        if not is_valid_email(email=email):
            errors['email'] = [
                'Некорректный адрес электронной почты'
            ]

        if attrs.get('password') != attrs.get('password2'):
            errors['password'] = ['Пароли не совпадают']
            errors['password2'] = ['Пароли не совпадают']

        if errors:
            serializer_logger(request=request, attrs=attrs, errors=errors)
            raise serializers.ValidationError(errors)

        return super().validate(attrs)

class UpdateConfirmationCodeIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(
        label='user_id', 
        write_only=True, 
        required=True
    )
    @validate_unexpected_fields()
    def validate(self, attrs):
        return attrs
        
class CheckConfirmationCodeIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(
        label='user_id', 
        write_only=True, 
        required=True
    )
    code = serializers.CharField(
        label='code', 
        write_only=True, 
        required=True,
        allow_blank=False
    )
    @validate_unexpected_fields()
    def validate(self, attrs):
        return attrs

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="email",
        write_only=True,
        required=True,
        allow_blank=False,
    )
    password = serializers.CharField(
        label="password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    @validate_unexpected_fields()
    def validate(self, attrs):
        errors = {}
        request = self.context['request']
        password = attrs.get('password')
        email = attrs.get('email')
        if not password:
            errors['password'] = ['Укажите пароль']

        if not email:
            errors['email'] = ['Введите email']
            
        if not is_valid_email(email=email):
            errors['email'] = 'Некорректный адрес электронной почты'

        if errors:
            serializer_logger(request=request, attrs=attrs, errors=errors)
            raise serializers.ValidationError(errors)

        return super().validate(attrs)
