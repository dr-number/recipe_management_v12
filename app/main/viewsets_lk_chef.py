from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema

from main.serializers_lk import (
    LkAllRecipesSerializer
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
            LkAllRecipesSerializer(
                RecipeCategory.objects.all().order_by('-created'), 
                many=True
            ).data
        )


