from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", views.login_view, name='login'),
    path("accounts/logout/", views.logout, name="logout"),
    path("accounts/register/", views.register_user, name="register"),
    path("accounts/profile/", views.profile, name="profile"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    
    
    
]