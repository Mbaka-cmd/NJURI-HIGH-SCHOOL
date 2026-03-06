from django.urls import path
from . import views

urlpatterns = [
    path("", views.timetable_list, name="timetable_list"),
    path("edit/<uuid:stream_id>/<int:year_id>/", views.timetable_edit, name="timetable_edit"),
    path("teacher/", views.teacher_timetable, name="teacher_timetable"),
    path("student/", views.student_timetable, name="student_timetable"),
]
