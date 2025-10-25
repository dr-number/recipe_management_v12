from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main import viewsets

router = DefaultRouter()
router.register('allow_any', viewsets.AllowAnyViewSet, basename='allow_any')

urlpatterns = [
    path('', include(router.urls)),
]
