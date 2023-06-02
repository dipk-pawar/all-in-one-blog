from django.urls import path
from .views import (
    Dashboard,
    DashboardCategories,
    AddCategories,
    EditCategory,
    DeleteCategory,
)

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("categories", DashboardCategories.as_view(), name="dashboard_categories"),
    path("add_category", AddCategories.as_view(), name="add_category"),
    path("edit/<int:pk>/", EditCategory.as_view(), name="edit_category"),
    path("delete/<int:pk>/", DeleteCategory.as_view(), name="delete_category"),
]
