from django.contrib import admin
from .models import Student, ParentGuardian, TeacherProfile

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["admission_number", "first_name", "last_name", "current_stream", "status", "is_boarder"]
    list_filter = ["status", "is_boarder", "gender", "current_stream"]
    search_fields = ["first_name", "last_name", "admission_number", "nemis_number"]

@admin.register(TeacherProfile)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["user", "tsc_number", "employment_type", "is_hod", "is_active"]
    search_fields = ["user__first_name", "user__last_name", "tsc_number"]

@admin.register(ParentGuardian)
class ParentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "relationship", "phone_primary"]
    search_fields = ["first_name", "last_name", "phone_primary"]