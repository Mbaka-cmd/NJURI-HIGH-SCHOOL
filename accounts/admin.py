from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "first_name", "last_name", "primary_role", "school", "is_active"]
    list_filter = ["is_teacher", "is_parent", "is_student", "is_school_admin", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone", "gender", "date_of_birth", "profile_photo")}),
        ("School", {"fields": ("school",)}),
        ("Roles", {"fields": ("is_platform_admin", "is_school_admin", "is_teacher", "is_parent", "is_student")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password1", "password2")}),
        ("Roles", {"fields": ("is_school_admin", "is_teacher", "is_parent", "is_student")}),
    )