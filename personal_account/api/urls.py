from api.views.auth import TokenView
from api.views.data_for_bot import DataForBot, DowntimeDataForBor
from api.views.lk import CalendarView
from api.views.users import GroupJobViewSet, UserViewSet
from api.views.downtime import DowntimeViewSet
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register("groupsjob", GroupJobViewSet)
router_v1.register("token", TokenView)
router_v1.register("downtime", DowntimeViewSet)

urlpatterns = [
    path("", include(router_v1.urls)),
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
    path("downtime-data-bot/", DowntimeDataForBor.as_view(), name="downtime_bot")
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
