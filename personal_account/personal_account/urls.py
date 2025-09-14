from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('api.urls')),
    path('lk/', include('lk.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]

handler500 = "utils.pages_error.server_error"
handler404 = "utils.pages_error.page_not_found"
handler403csrf = "utils.pages_error.csrf_permission_denied"
