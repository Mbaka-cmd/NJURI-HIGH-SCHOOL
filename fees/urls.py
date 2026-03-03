from django.urls import path
from . import views

urlpatterns = [
    path("", views.fee_dashboard, name="fee_dashboard"),
    path("invoices/", views.invoice_list, name="invoice_list"),
    path("invoices/generate/", views.generate_invoices, name="generate_invoices"),
    path("invoices/<uuid:pk>/", views.invoice_detail, name="invoice_detail"),
    path("payments/record/<uuid:pk>/", views.record_payment, name="record_payment"),
    path("mpesa/stk-push/<uuid:pk>/", views.mpesa_stk_push, name="mpesa_stk_push"),
    path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
]