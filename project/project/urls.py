from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # App API Endpoints
    path("api/", include("app.urls")),

    # JWT Authentication Routes
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# React Frontend Route (Catch-all) — Must be last
urlpatterns += [
    re_path(r"^.*$", TemplateView.as_view(template_name="index.html")),
]
