from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema

from main.serializers_lk import (
    LkAllChefCategoriesRecipesSerializer, LkChefAddRecipeInputSerializer, 
    LkChefUpdateRecipeInputSerializer
)
from main.models import RecipeCategory, Recipe
from main.const import CodesErrors
from main.helpers import get_recipe_category_params, get_recipe_params
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

    @swagger_auto_schema(request_body=LkChefAddRecipeInputSerializer)
    @action(detail=False, methods=['post'])
    def add_recipe(self, request):
        serializer = LkChefAddRecipeInputSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe_category = get_recipe_category_params(data={
            'id': serializer.validated_data['id_category_recipe']
        })
        if not recipe_category:
             return log_error_response(request, {
                'errorText': 'Категория не найдена!'
            })

        new_recipe = Recipe.objects.create(
            title=serializer.validated_data['title'],
            html_description=serializer.validated_data['html_description'],
            ingredients=serializer.validated_data['ingredients'],
            steps=serializer.validated_data['steps'],
            time_cooking=serializer.validated_data['time_cooking'],
            type=recipe_category,
            user=request.user
        )

        return Response({
            'recipe_id': new_recipe.pk
        })

    @swagger_auto_schema(request_body=LkChefUpdateRecipeInputSerializer)
    @action(detail=False, methods=['post'])
    def update_recipe(self, request):
        serializer = LkChefUpdateRecipeInputSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe: Recipe = get_recipe_params(params={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.ERROR_HELP,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        recipe_category = get_recipe_category_params(data={
            'id': serializer.validated_data['id_category_recipe']
        })
        if not recipe_category:
             return log_error_response(request, {
                'errorText': 'Категория не найдена!'
            })

        recipe['title']=serializer.validated_data['title']
        recipe['html_description']=serializer.validated_data['html_description']
        recipe['ingredients']=serializer.validated_data['ingredients']
        recipe['steps']=serializer.validated_data['steps']
        recipe['time_cooking']=serializer.validated_data['time_cooking']
        recipe['type']=recipe_category
        recipe.save()

        return Response('ok')

