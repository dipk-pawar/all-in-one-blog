from django.urls import path
from accounts.views import UserRegister

urlpatterns = [
    path("register", UserRegister.as_view(), name="register_user"),
]
