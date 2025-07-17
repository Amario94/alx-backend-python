# from django.urls import path, include
# from django.contrib import admin
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from django.views.generic import RedirectView

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Messaging API",
#         default_version='v1',
#         description="API documentation for your messaging app",
#         terms_of_service="https://www.yourcompany.com/terms/",
#         contact=openapi.Contact(email="support@yourcompany.com"),
#         license=openapi.License(name="MIT License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

# urlpatterns = [
#     path('', RedirectView.as_view(url='/swagger/', permanent=False)),
#     path('admin/', admin.site.urls),

#     # 👇 Include the URLs from your `chats` app
#     path('', include('chats.urls')),

#     # Swagger/OpenAPI
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="Messaging API",
        default_version='v1',
        description="API documentation for your messaging app",
        terms_of_service="https://www.yourcompany.com/terms/",
        contact=openapi.Contact(email="support@yourcompany.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Expose API under /api/
    path('api/', include('chats.urls')),

    # Swagger/OpenAPI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # 👇 Redirect root path to Swagger
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
]
