from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema

from main.serializers_lk import (
    LkAllRecipesSerializer, LkRecipeSerializer, LkRecipeInputSerializer
)
from main.models import Recipe
from main.const import CodesErrors
from main.helpers import get_recipe_params
from app.helpers import log_error_response


class LkAllViewSet(ViewSet):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes =(permissions.IsAuthenticated,)

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def list_all_recipes(self, request):
        return Response(
            LkAllRecipesSerializer(
                Recipe.objects.all().order_by('-created'), 
                many=True
            ).data
        )

    @swagger_auto_schema(request_body=LkRecipeInputSerializer)
    @action(detail=False, methods=['get'])
    def get_recipe(self, request):
        query_params = request.query_params.dict()
        serializer = LkRecipeInputSerializer(data=query_params, context={'request': request})
        
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe = get_recipe_params(params={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.ERROR_HELP,
                'errorText': (
                    'Данный запрос в техподдержку не найден!'
                )
            })

        return Response(
            LkRecipeSerializer(recipe).data
        )