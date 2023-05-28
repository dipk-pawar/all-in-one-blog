from django.urls import path
from blog_app.views import PostsByCategory

urlpatterns = [
    path("<int:id>", PostsByCategory.as_view(), name="post_by_category"),
]
