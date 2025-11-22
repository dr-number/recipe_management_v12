import traceback
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import login


from main.serializers import (
    CreateAccountSerializer, CheckConfirmationCodeIdSerializer, LoginSerializer, 
    UpdateConfirmationCodeIdSerializer, AddFeedbackSerializer
)
from main.models import User, Feedback
from main.const import CodesErrors
from main.helpers import send_email_code, get_user_params, is_base64
from app.helpers import log_error_response

from django.shortcuts import render
from django.template.loader import render_to_string

from main.aes import aes_decrypt
from app.help_logger import logger
from app.settings import IMG_PASSWORD

class AllowAnyViewSet(ViewSet):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes =(permissions.AllowAny,)

    @swagger_auto_schema(request_body=CreateAccountSerializer)
    @action(detail=False, methods=['post'])
    def create_account(self, request):
        serializer = CreateAccountSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].lower()
        first_name = serializer.validated_data['first_name'].lower().capitalize()
        last_name = serializer.validated_data['last_name'].lower().capitalize()

        if User.objects.filter(is_active=True, username=email, is_confirmed_email=True).exists():
            return log_error_response(request, {
                'errorText': (
                    'Активная учетная запись с таким email уже зарегистрирована!'
                )}
            )

        no_active_users = User.objects.filter(is_active=False, username=email)
        if no_active_users:
            no_active_users.delete()

        new_user: User = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            type=serializer.validated_data['type'],
            password=serializer.validated_data['password']
        )
        is_send_email, _, _ = send_email_code(user=new_user)

        return Response({
            'id': new_user.id,
            'is_active': new_user.is_active,
            'is_confirmed_email': new_user.is_confirmed_email,
            'is_send_email': is_send_email
        })

    @swagger_auto_schema(request_body=UpdateConfirmationCodeIdSerializer)
    @action(detail=False, methods=['post'])
    def update_confirmation_code_id(self, request):
        serializer = UpdateConfirmationCodeIdSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = get_user_params(data={
            'id': serializer.validated_data['user_id']
        })
        if not user:
            return log_error_response(request, {
                'errorText': (
                    'Пользователь не найден!'
                )
            })

        is_send_email, _, _ = send_email_code(user=user)
        return Response({
            'is_send_email': is_send_email
        })


    @swagger_auto_schema(request_body=CheckConfirmationCodeIdSerializer)
    @action(detail=False, methods=['post'])
    def check_confirmation_code_id(self, request):
        serializer = CheckConfirmationCodeIdSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user: User = get_user_params({
            'id': serializer.validated_data['user_id'],
            'is_confirmed_email': False
        })
        if not user:
             return log_error_response(request, {
                'errorText': 'Пользователь не найден!'
            })
            
        is_success = user.check_confirmation_code(
            check_code=serializer.validated_data['code']
        )
        
        if is_success:
            user.is_confirmed_email = True
            user.is_active = True
            user.save(update_fields=['is_confirmed_email', 'is_active'])
            return Response({
                'is_active': user.is_active,
                'is_confirmed_email': user.is_confirmed_email,
                'token': user.token.key
            })

        return log_error_response(request, {
            'errorText': 'Код подтверждения недействителен. Пожалуйста, убедитесь в правильности введенного кода'
        })

    @swagger_auto_schema(request_body=LoginSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email', '').lower()
        password = serializer.validated_data['password']

        user: User = get_user_params({
            'is_active': True,
            'is_confirmed_email': True,
            'email': email,
        })

        if not user or not user.is_active:
            return log_error_response(request, {
                'errorText': 'Пользователь с такими данными не зарегистрирован. Проверьте логин.'
            })

        if user and user.is_active and user.check_password(password):
            login(request, user)
            return Response({
                'token': user.token.key,
            })

        return log_error_response(request, {
            'errorText': 'Введены неверные данные проверьте пароль'
        })

    @swagger_auto_schema(request_body=AddFeedbackSerializer)
    @action(detail=False, methods=['post'])
    def add_feedback(self, request):
        serializer = AddFeedbackSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        Feedback.objects.create(
            email=serializer.validated_data.get('email', '').lower(),
            text=serializer.validated_data['text']
        )
        return Response('ok')


def custom_page_404(request, exception):
    not_decrypt = render_to_string('includes/img_404.html')
    try:
        img = aes_decrypt(not_decrypt, password=IMG_PASSWORD)
        if not is_base64(text=img):
            img = ''
    except Exception as e:
        logger.error(f'Error: {e}\n\n{traceback.format_exc()}')
        img = ''

    return render(request, 'page404.html', context={
            'img': img,
            # 'not_decrypt': not_decrypt
        }, status=404)
