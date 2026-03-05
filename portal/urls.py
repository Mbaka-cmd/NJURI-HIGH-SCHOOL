from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal_redirect, name='portal_redirect'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/results/', views.student_results, name='student_results'),
    path('student/fees/', views.student_fees, name='student_fees'),
    path('parent/', views.parent_dashboard, name='parent_dashboard'),
    path('parent/student/<uuid:student_id>/', views.parent_student_detail, name='parent_student_detail'),
]