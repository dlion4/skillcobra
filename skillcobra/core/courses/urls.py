from django.urls import path

from .views import CourseDetailView
from .views import course_handle_like_click_view
from .views import course_handle_unlike_click_view
from .views import add_course_to_cart_view, remove_course_from_cart

app_name = "courses"
urlpatterns = [
    path(
        "<pk>/<slug>/",
        CourseDetailView.as_view(),
        name="course_detail_view",
    ),
    path(
        "<course_pk>/<course_slug>/like/",
        course_handle_like_click_view,
        name="course_like_view",
    ),
    path(
        "<course_pk>/<course_slug>/unlike/",
        course_handle_unlike_click_view,
        name="course_unlike_view",
    ),
    path(
        "<course_pk>/<course_slug>/add-to-cart/",
        add_course_to_cart_view,
        name="add_course_to_cart",
    ),
    path(
        "<course_pk>/<course_slug>/remove-from-cart/",
        remove_course_from_cart,
        name="remove_course_from_cart",
    ),
]
