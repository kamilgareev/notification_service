from django.urls import path, include
from rest_framework import routers
from .views import ClientViewSet, DistributionViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'distributions', DistributionViewSet, basename='distribution')

schema_view = get_schema_view(
    openapi.Info(
        title='Notification service API',
        default_version='v1',
        description='Notification service API documentation'
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
]
