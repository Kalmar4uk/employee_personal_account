from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework import routers

from api.views.auth import TokenView, TokenViewV2
from api.views.data_for_bot import DataForBot
from api.views.downtime import DowntimeViewSet, DowntimeViewSetV2
from api.views.lk import CalendarView
from api.views.users import GroupJobViewSet, UserViewSet, UserViewSetV2

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register("groupsjob", GroupJobViewSet)
router_v1.register("token", TokenView)
router_v1.register("downtime", DowntimeViewSet)

router_v2 = routers.DefaultRouter()
router_v2.register("token", TokenViewV2)
router_v2.register("downtime", DowntimeViewSetV2)
router_v2.register("users", UserViewSetV2)

urlpatterns = [
    path("", include(router_v1.urls)),
    path("v2/", include(router_v2.urls)),
    path(
        "calendar/users/<int:user_id>/",
        CalendarView.as_view({"get": "user"}),
        name="user_calendar"
    ),
    path(
        "calendar/groups/<int:group_id>/",
        CalendarView.as_view({"get": "group"}),
        name="group_calendar"
    ),
    path("data-for-bot/", DataForBot.as_view(), name="bot"),
]

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs"
    ),
    path("redoc/", SpectacularRedocView.as_view(), name="docs_redoc")
]
