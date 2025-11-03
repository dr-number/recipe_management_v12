from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions, parsers, renderers
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from django.template.loader import render_to_string

from main.serializers_lk import (
    LkAllRecipesSerializer, RecipeWithCommentsSerializer, LkRecipeInputSerializer, 
    LkRecipeAddCommentInputSerializer, LkAllCommentsSerializer, LkAllUserOutputSerializer
)
from main.models import Recipe, Comment, User
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

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def get_user_info(self, request):
        return Response(
            LkAllUserOutputSerializer(
                request.user
            ).data
        )

    @action(detail=False, methods=['get'])
    def get_lk(self, request):
        return render(request, 'lk.html', {
            'user': LkAllUserOutputSerializer(request.user).data,
            
        })
    
    @action(detail=False, methods=['get'])
    def get_lk_list_all_recipes(self, request):
        list_all_recipes = LkAllRecipesSerializer(
            Recipe.objects.all().order_by('-created'), 
            many=True
        ).data

        recipes = ''
        for item in list_all_recipes:
            recipes += render_to_string('includes/items/recipt.html', {
                    'item' : item
            })
            
        return render(request, 'includes/list_all_recipes.html', {
            'recipes': recipes
        })

    # @swagger_auto_schema(request_body=LkRecipeInputSerializer)
    @action(detail=False, methods=['get'])
    def get_recipe(self, request):
        query_params = request.query_params.dict()
        serializer = LkRecipeInputSerializer(data=query_params, context={'request': request})
        
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe: Recipe = get_recipe_params(data={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        return Response(RecipeWithCommentsSerializer(recipe).data)


    @swagger_auto_schema(request_body=LkRecipeAddCommentInputSerializer)
    @action(detail=False, methods=['post'])
    def add_comment_to_recipe(self, request):
        serializer = LkRecipeAddCommentInputSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe = get_recipe_params(data={
            'id': serializer.validated_data['id_recipe']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        new_comment = Comment.objects.create(
            recipe=recipe,
            raiting=serializer.validated_data['raiting'],
            text=serializer.validated_data['text'],
            user=request.user
        )

        return Response({
            'comment_id': new_comment.pk
        })

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def get_list_my_comments(self, request):
        return Response(
            LkAllCommentsSerializer(
                Comment.objects.filter(user=request.user).order_by('-created'), 
                many=True
            ).data
        )

    @swagger_auto_schema(request_body=LkRecipeInputSerializer)
    @action(detail=False, methods=['post'])
    def add_recipe_to_favorite(self, request):
        serializer = LkRecipeInputSerializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            return Response({'code': CodesErrors.UNKNOWN_VALIDATION_ERROR, **serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        recipe = get_recipe_params(data={
            'id': serializer.validated_data['id']
        })

        if not recipe:
            return log_error_response(request, {
                'code': CodesErrors.NOT_FOUND,
                'errorText': (
                    'Данный рецепт не найден!'
                )
            })

        user: User = request.user
        user.favorites.add(recipe)

        return Response('ok')

    @swagger_auto_schema()
    @action(detail=False, methods=['get'])
    def get_list_my_favorites(self, request):
        user: User = request.user
        return Response(
            LkAllRecipesSerializer(
                user.favorites.order_by('-created'), 
                many=True
            ).data
        )
