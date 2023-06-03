from django import forms
from blog_app.models import Category, Blog
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "featured_image",
            "short_description",
            "blog_body",
            "status",
            "is_featured",
        )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
