from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema

from main.serializers import CreateAccountSerializer
from main.models import User
from main.const import CodesErrors
from main.helpers import send_email_code

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

        if User.objects.filter(is_active=True, email=email, is_confirmed_email=True).exists():
            return Response({
                'errorText': (
                    'Активная учетная запись с таким email уже зарегистрирована!'
                )},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_user = User.objects.create_user(
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
