from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/auth/login/", include("login.urls")),
    path("api/v1/auth/register/", include("register.urls")),
]
