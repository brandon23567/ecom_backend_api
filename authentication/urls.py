from . import views
from django.urls import path 

urlpatterns = [
    path("signup/", views.signup_user, name="signup_user"),
    path("signin/", views.signin_user, name="signin_user"),
    path("current_user/", views.get_current_user, name="current_user"),
]
