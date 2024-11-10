from django.urls import path

from . import views

urlpatterns = [
    path("categories", views.CategoryApiView.as_view()),  # List of categories
    path(
        "categories/<int:category_pk>/", views.CategoryApiView.as_view(),
    ),  # Retrieve or update a single category
    path(
        "categories/<int:category_pk>/sub/", views.SubCategoryModelAPIView.as_view(),
    ),  # Subcategories for a category
    path(
        "categories/<int:category_pk>/sub/<int:subcategory_pk>/",
        views.SubCategoryModelAPIView.as_view(),
    ),  # Single subcategory
]
