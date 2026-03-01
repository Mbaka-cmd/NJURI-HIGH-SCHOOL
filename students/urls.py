from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("add/", views.student_add, name="student_add"),
    path("<uuid:pk>/", views.student_detail, name="student_detail"),
    path("<uuid:pk>/edit/", views.student_edit, name="student_edit"),
]