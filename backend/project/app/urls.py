from django.urls import path, re_path
from . import views

urlpatterns = [

    # ---------------------------
    # Health Check / Default Route
    # ---------------------------
    path("", views.health_check, name="health_check"),

    # ---------------------------
    # Authentication Endpoints
    # ---------------------------
    path("register/", views.register_user, name="register_user"),
    path("login/", views.session_login, name="session_login"),
    path("logout/", views.user_logout, name="logout"),

    # ---------------------------
    # Applicant + Table Data
    # ---------------------------
    path("getApplicantsData/", views.get_connections, name="get_connections"),
    re_path(r"^getApplicantsData$", views.get_connections),   # Accepts no-slash version
    path("updateApplicant/<int:id>/", views.update_applicant, name="update_applicant"),

    # ---------------------------
    # CSV Upload Route
    # ---------------------------
    path("uploadData/", views.uploaddata, name="upload_data"),
]
