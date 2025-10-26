from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main import viewsets, viewsets_lk, view_front

router = DefaultRouter()
router.register('allow_any', viewsets.AllowAnyViewSet, basename='allow_any')
router.register('lk_all', viewsets_lk.LkAllViewSet, basename='lk_all')

urlpatterns = [
    path('', include(router.urls)),
    path('front/register/', view_front.CreateAccountWebView.as_view(), name='front_register'),
    path('front/loginin/', view_front.LogininWebView.as_view(), name='front_loginin'),
]
