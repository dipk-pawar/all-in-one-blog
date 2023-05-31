from django.shortcuts import render, redirect
from django.views import View
from blog_app.models import Category, Blog, About
from django.db.models import Q


# Create your views here.
class Home(View):
    def get(self, request):
        blogs = Blog.objects.filter(status="Published").order_by("-updated_at")
        about = About.objects.last()
        return render(request, "home.html", context={"blogs": blogs, "about": about})


class GetPostBySlug(View):
    def get(self, request, slug):
        blog = Blog.objects.get(status="Published", slug=slug)
        return render(request, "blog_post.html", context={"post": blog})


class PostsByCategory(View):
    def get(self, request, id):
        try:
            blogs = Blog.objects.filter(status="Published", category_id=id).order_by(
                "-updated_at"
            )
            category = blogs[0].category if blogs else Category.objects.get(id=id)
        except Exception:
            return redirect("home")
        return render(
            request,
            "category_post.html",
            context={"category": category, "blogs": blogs},
        )


class SearchCategory(View):
    def get(self, request):
        searched_posts = []
        keyword = request.GET.get("keyword")
        if keyword and keyword.strip() != "":
            searched_posts = Blog.objects.filter(
                Q(title__icontains=keyword)
                | Q(short_description__icontains=keyword)
                | Q(blog_body__icontains=keyword),
                status="Published",
            )
        else:
            searched_posts = Blog.objects.filter(status="Published")
        return render(
            request,
            "searched_posts.html",
            context={"searched_posts": searched_posts, "keyword": keyword},
        )
