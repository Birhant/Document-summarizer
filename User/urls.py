from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('profile/', views.profile, name="Profile"),
    path('signup/', views.signup, name="Signup"),
    path('login/', views.login_view, name="Login"),
    path('signout/', views.signout, name="Signout"),
    path('change_password/', views.change_password, name="ChangePassword"),
]




