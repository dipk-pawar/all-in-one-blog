from django.shortcuts import render
from django.views import View
from blog_app.models import Category


# Create your views here.
class Home(View):
    def get(self, request):
        tags = Category.objects.select_related().all()
        return render(request, "home.html", context={"tags": tags})
