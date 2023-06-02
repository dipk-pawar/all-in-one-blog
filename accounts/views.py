from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


# Create your views here.
class UserRegister(View):
    def get(self, request):
        registration_form = RegistrationForm()
        return render(
            request, "accounts/register.html", context={"form": registration_form}
        )

    def post(self, request):
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            try:
                registration_form.save()
                messages.success(request, "User Registered successfully")
                return redirect("login_user")
            except Exception:
                messages.error(request, "Sorry, something went wrong")
                return redirect("register_user")
        return render(
            request, "accounts/register.html", context={"form": registration_form}
        )


class UserLogin(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, "accounts/login.html", context={"form": login_form})

    def post(self, request):
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            try:
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                if user := auth.authenticate(username=username, password=password):
                    auth.login(request, user)
                    return redirect("dashboard")
                messages.error(request, "Sorry, Username or password is incorrect")
                return redirect("login_user")
            except Exception:
                messages.error(request, "Sorry, something went wrong")
                return redirect("login_user")
        return render(request, "accounts/login.html", context={"form": login_form})


class UserLogout(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "User, logged out successfully")
        return redirect("login_user")
