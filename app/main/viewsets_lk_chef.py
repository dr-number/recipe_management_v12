from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema

from main.serializers_lk import (
    LkAllChefCategoriesRecipesSerializer
)
from main.models import RecipeCategory
from main.const import CodesErrors
from main.helpers import get_recipe_params
from app.helpers import log_error_response

from main.permissions import IsChefUser


class LkChefViewSet(ViewSet):
    throttle_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes =(permissions.IsAuthenticated, IsChefUser)

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def list_all_recipe_categories(self, request):
        return Response(
            LkAllChefCategoriesRecipesSerializer(
                RecipeCategory.objects.all().order_by('-created'), 
                many=True
            ).data
        )

    @swagger_auto_schema(request_body=LkAllChefCategoriesRecipesSerializer)
    @action(detail=False, methods=['post'])
    def add_recipe(self, request):
        serializer = LkAllChefCategoriesRecipesSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


