from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("search/", views.global_search, name="global_search"),
]