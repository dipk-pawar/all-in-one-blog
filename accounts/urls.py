from django.urls import path
from accounts.views import UserRegister, UserLogin, UserLogout

urlpatterns = [
    path("register", UserRegister.as_view(), name="register_user"),
    path("login", UserLogin.as_view(), name="login_user"),
    path("logout", UserLogout.as_view(), name="logout_user"),
]
