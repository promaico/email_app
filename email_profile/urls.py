from django.urls import path, include
from django.contrib.auth import views
from . import views
from .views import *


urlpatterns = [
    path("accounts/profile/", views.profile, name="profile" ),
]

