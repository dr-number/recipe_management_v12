from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(f'admin/', admin.site.urls),
    path('main/', include('main.urls')),
    # path('payments/', include('payments.urls')),
    # path('documents/', include('documents.urls'))
]


if True or IS_TEST_SERVER:
    urlpatterns.append(
        path(
            'swagger_doc/', 
            schema_view.with_ui('swagger', cache_timeout=0), 
            name='swagger_doc'
        )
    )

# urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
