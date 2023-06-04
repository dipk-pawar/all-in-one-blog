from django.urls import path
from blog_app.views import (
    PostsByCategory,
    GetPostBySlug,
    SearchCategory,
)

urlpatterns = [
    path("<int:id>", PostsByCategory.as_view(), name="post_by_category"),
    path("<slug:slug>", GetPostBySlug.as_view(), name="post_by_slug"),
    path("search/", SearchCategory.as_view(), name="search_category"),
]
