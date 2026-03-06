from django.urls import path
from . import views

urlpatterns = [
    path("bulk-sms/", views.bulk_sms, name="bulk_sms"),
]
