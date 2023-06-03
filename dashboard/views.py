from django.shortcuts import render, redirect
from django.views import View
from blog_app.models import Category, Blog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from .forms import CategoryForm, BlogForm, UserRegistrationForm, EditUserForm
from django.contrib import messages
from django.template.defaultfilters import slugify
import uuid
from django.contrib.auth.models import User
from .permission_decorator import manager_or_admin_required, editor_or_admin_required


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
@method_decorator(editor_or_admin_required, name="dispatch")
class DashboardCategories(TemplateView):
    template_name = "dashboard/categories/categories.html"


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
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


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
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


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
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


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
class DashboardPosts(TemplateView):
    template_name = "dashboard/posts/dashboard_posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Blog.objects.all()
        context["posts"] = posts
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
class DashboardAddPost(View):
    def get(self, request):
        form = BlogForm()
        return render(request, "dashboard/posts/add_post.html", {"form": form})

    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                return self.create_post_func(form, request)
            except Exception:
                messages.error(request, "Sorry, something went wrong")
                return redirect("dashboard_add_post")
        else:
            messages.error(request, "Sorry, Something went wrong")
            return redirect("dashboard_add_post")

    def create_post_func(self, form, request):
        title = form.cleaned_data["title"]
        post = form.save(commit=False)
        post.author = request.user
        post.slug = f"{slugify(title)}-{str(uuid.uuid4())}"
        post.save()
        messages.success(request, "Blog post added successfully")
        return redirect("dashboard_posts")


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
class DashboardEditPost(View):
    def get(self, request, pk):
        try:
            blog_post = Blog.objects.get(id=pk)
            form = BlogForm(instance=blog_post)
            return render(
                request,
                "dashboard/posts/edit_post.html",
                {"form": form, "blog_post": blog_post},
            )
        except Exception:
            messages.error(request, "Sorry, something went wrong")
            return redirect("dashboard_posts")

    def post(self, request, pk):
        try:
            blog_post = Blog.objects.get(id=pk)
        except Exception:
            messages.error(request, "Sorry, The post is not available")
            return redirect("dashboard_posts")
        form = BlogForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            try:
                return self.update_post_func(form, request)
            except Exception:
                messages.error(request, "Sorry, something went wrong")
                return redirect("dashboard_add_post")
        else:
            messages.error(request, "Sorry, Something went wrong")
            return redirect("dashboard_add_post")

    def update_post_func(self, form, request):
        title = form.cleaned_data["title"]
        post = form.save(commit=False)
        post.author = request.user
        post.slug = f"{slugify(title)}-{str(uuid.uuid4())}"
        post.save()
        messages.success(request, "Blog post added successfully")
        return redirect("dashboard_posts")


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
class DeleteDashboardPost(View):
    def get(self, request, pk):
        try:
            blog_post = Blog.objects.get(id=pk)
            blog_post.delete()
            messages.success(request, "Blog post deleted successfully")
            return redirect("dashboard_posts")
        except Exception:
            messages.error(request, "Sorry, post not found")
            return redirect("dashboard_posts")


@method_decorator(login_required, name="dispatch")
@method_decorator(manager_or_admin_required, name="dispatch")
class DashboardUsers(TemplateView):
    template_name = "dashboard/users/dashboard_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context["users"] = users
        return context


@method_decorator(login_required, name="dispatch")
class NoPermissionPage(TemplateView):
    template_name = "dashboard/no_permission.html"


@method_decorator(login_required, name="dispatch")
@method_decorator(manager_or_admin_required, name="dispatch")
class GetandCreateDashboardUser(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(
            request, "dashboard/users/dashboard_add_user.html", {"form": form}
        )

    def post(self, request):
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "User added successfully")
                return redirect("dashboard_users")
            else:
                messages.error(request, "Sorry, something went wrong")
                return redirect("add_dashboard_user")
        except Exception:
            messages.error(request, "Sorry, Something went wrong")
            return redirect("add_dashboard_user")


@method_decorator(login_required, name="dispatch")
@method_decorator(manager_or_admin_required, name="dispatch")
class RetrieveandDeleteUser(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            form = EditUserForm(instance=user)
            return render(
                request,
                "dashboard/users/edit_dashboard_user.html",
                {"form": form, "user": user},
            )
        except Exception:
            messages.error(request, "Sorry, user not found")
            return redirect("dashboard_users")

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            form = EditUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "User updated successfully")
                return redirect("dashboard_users")
            else:
                messages.error(request, "Sorry, something went wrong")
                return redirect("dashboard_edit_user", pk=pk)
        except Exception:
            messages.error(request, "Sorry, Something went wrong")
            return redirect("dashboard_edit_user", pk=pk)


@method_decorator(login_required, name="dispatch")
@method_decorator(editor_or_admin_required, name="dispatch")
class DeleteDashboardUsers(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user.delete()
            messages.success(request, "User deleted successfully")
            return redirect("dashboard_users")
        except Exception:
            messages.error(request, "Sorry, user not found")
            return redirect("dashboard_users")
