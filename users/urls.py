from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from . import views
from .views import *
from users.forms import LoginForm

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", views.login_view, name='login'),
    path("accounts/logout/", views.logout, name="logout"),
    path("accounts/register/", views.register_user, name="register"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path("accounts/profile/", views.profile, name="profile" ),
    path("accounts/profile/emails/", views.profile_email, name="profile_email"),
    path("accounts/profile_creation/", views.profile_creation, name="profile_creation" ),
    path("accounts/first_login/", views.first_login_view, name="first_login_view"),
    
]