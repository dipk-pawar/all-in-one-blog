from django.urls import path
from .views import (
    Dashboard,
    DashboardCategories,
    AddCategories,
    EditCategory,
    DeleteCategory,
    DashboardPosts,
    DashboardAddPost,
    DashboardEditPost,
    DeleteDashboardPost,
)

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("categories", DashboardCategories.as_view(), name="dashboard_categories"),
    path("add_category", AddCategories.as_view(), name="add_category"),
    path("edit/<int:pk>/", EditCategory.as_view(), name="edit_category"),
    path("delete/<int:pk>/", DeleteCategory.as_view(), name="delete_category"),
    path("posts", DashboardPosts.as_view(), name="dashboard_posts"),
    path("posts/add/", DashboardAddPost.as_view(), name="dashboard_add_post"),
    path(
        "posts/edit/<int:pk>/", DashboardEditPost.as_view(), name="dashboard_edit_post"
    ),
    path("posts/delete/<int:pk>/", DeleteDashboardPost.as_view(), name="delete_post"),
]
