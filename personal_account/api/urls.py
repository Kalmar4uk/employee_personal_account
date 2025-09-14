from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import GroupJobViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register("groupsjob", GroupJobViewSet)

urlpatterns = [
    path("", include(router_v1.urls))
]


schema_view = get_schema_view(
   openapi.Info(
      title="LK API",
      default_version='v1',
      description="Документация для проекта LK",
      contact=openapi.Contact(email="admin@lk.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
