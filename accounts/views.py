from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm


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
            registration_form.save()
            return redirect("home")
        return render(
            request, "accounts/register.html", context={"form": registration_form}
        )
