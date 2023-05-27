from django.shortcuts import render
from django.views import View
from blog_app.models import Category, Blog


# Create your views here.
class Home(View):
    def get(self, request):
        tags = Category.objects.all()
        blogs = Blog.objects.filter(status="Published").order_by("-updated_at")
        return render(request, "home.html", context={"tags": tags, "blogs": blogs})
