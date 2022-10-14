from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('login/',views.login_user, name="login"),
    path('signup/',views.signUp, name="signup"),
    path('logout',views.logout_user, name="logout")
]
