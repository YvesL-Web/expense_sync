from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/bank/", include("apps.bank_accounts.urls")),
]
