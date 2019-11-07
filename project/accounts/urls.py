from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
 path('',LoginView.as_view(template_name='accounts/home.html'),name="accounts"),
 path('login/',LoginView.as_view(template_name='accounts/login.html'),name="login"),
 path('logout/',views.logout_request,name="logout"),
 path('register/',views.signup,name="register"),
 path('user/',views.user,name="user"),
 path('change/',views.change_password,name="change"),
 path('home/',views.home,name="home"),
 path('export/',views.export,name="export"),
]

