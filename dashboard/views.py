from django.shortcuts import render
from django.views import View
from blog_app.models import Category, Blog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
