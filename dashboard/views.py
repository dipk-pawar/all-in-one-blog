from django.shortcuts import render, redirect
from django.views import View
from blog_app.models import Category, Blog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from .forms import CategoryForm
from django.contrib import messages


# Create your views here..
@method_decorator(login_required, name="dispatch")
class Dashboard(View):
    def get(self, request):
        cat_count = Category.objects.all().count()
        post_count = Blog.objects.all().count()
        return render(
            request,
            "dashboard/dashboard.html",
            {"total_tags": cat_count, "total_posts": post_count},
        )


@method_decorator(login_required, name="dispatch")
class DashboardCategories(TemplateView):
    template_name = "dashboard/categories/categories.html"


@method_decorator(login_required, name="dispatch")
class AddCategories(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, "dashboard/categories/add_category.html", {"form": form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Category added successfully")
                return redirect("dashboard_categories")
            except Exception:
                messages.error(request, "Sorry, something went wrong")
                return redirect("add_category")
        else:
            return redirect("add_category")


class EditCategory(View):
    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            form = CategoryForm(instance=category)
            return render(
                request,
                "dashboard/categories/edit_category.html",
                {"form": form, "category": category},
            )
        except Exception:
            messages.error(request, "Sorry, category not found")
            return redirect("dashboard_categories")

    def post(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Category updated successfully")
                return redirect("dashboard_categories")
        except Exception:
            messages.error(request, "Sorry, something went wrong")
            return redirect("edit_category", pk=pk)


class DeleteCategory(View):
    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            category.delete()
            messages.success(request, "Category deleted successfully")
            return redirect("dashboard_categories")
        except Exception:
            messages.error(request, "Sorry, category not found")
            return redirect("dashboard_categories")
