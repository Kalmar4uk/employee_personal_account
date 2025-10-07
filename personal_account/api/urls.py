from api.views.auth import TokenView
from api.views.data_for_bot import DataForBot
from api.views.lk import CalendarView
from api.views.users import GroupJobViewSet, UserViewSet
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet)
router_v1.register("groupsjob", GroupJobViewSet)
router_v1.register("token", TokenView)

urlpatterns = [
    path("", include(router_v1.urls)),
    path(
        "calendar/user/<int:user_id>/",
        CalendarView.as_view({"get": "user"}),
        name="user_calendar"
    ),
    path(
        "calendar/user/<int:group_id>/",
        CalendarView.as_view({"get": "group"}),
        name="group_calendar"
    ),
    path("data-for-bot/", DataForBot.as_view(), name="bot")
]

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs"
    ),
]
