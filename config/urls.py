from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="ECOMMERSE API",
        default_version="v1",
        description="Test description",
        terms_of_service="Come On Man",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

    path('users/', include('users.urls')),
    path('', include('delivery.urls')),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
