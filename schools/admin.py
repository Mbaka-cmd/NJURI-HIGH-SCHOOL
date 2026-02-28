from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import School, AcademicYear, Term

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "county", "subscription_plan", "is_active", "current_year", "current_term"]
    list_filter = ["subscription_plan", "is_active", "gender_type", "category"]
    search_fields = ["name", "county", "town"]
    prepopulated_fields = {"slug": ["name"]}

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ["school", "year", "is_current", "start_date", "end_date"]
    list_filter = ["is_current"]

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ["academic_year", "number", "is_current", "start_date", "end_date"]