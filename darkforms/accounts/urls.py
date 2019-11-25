from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
 path('',LoginView.as_view(template_name='home.html'),name="accounts"),
 path('login/',LoginView.as_view(template_name='login.html'),name="login"),
 path('logout/',views.logout_request,name="logout"),
 path('register/',views.signup,name="register"),
 path('user/',views.user,name="user"),
 path('change/',views.change_password,name="change"),
 path('home/',views.home,name="home"),
 path('createform/', views.createform, name="create-form"),
 path('formlist/', views.formlist, name= "form-list"),
 path('displayform/<pk>', views.displayform, name="display-form"),
 path('answerform/<pk>', views.answerform, name="answer-form"),
 path('formlist/<pk>', views.answerform, name="flist"),
 path('entercode/', views.entercode, name = "enter-code"),
 path('question/<pk>',views.visual, name="question"),
 path('export/<pk>',views.export,name="export"),
 #path('viewusers/<pk>/', views.viewusers, name = "view-users"),
 #path('detailedresponse/<f>/<u>', views.detailedresponse, name = "detailed-response"),
]