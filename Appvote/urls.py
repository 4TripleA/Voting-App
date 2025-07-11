from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import CustomLogoutView


urlpatterns = [
    path("", auth_views.LoginView.as_view(next_page='index'), name="login"), 
    path("index/", views.index, name="index"),
    path("home/<str:slug>", views.home, name="home"),
    path("result/<str:slug>", views.result, name="result"),
    path("register/", views.register, name="register"),
    # path("logout/", LogoutView.as_view(), name="logout")
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]