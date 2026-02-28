from django.contrib import admin
from .models import Subject, SubjectCategory, ClassLevel, Stream, StreamSubject

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ["name", "school", "level_order"]
    ordering = ["school", "level_order"]

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ["full_name", "school", "class_teacher", "capacity"]
    list_filter = ["class_level"]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "school", "is_compulsory", "is_kcse_subject"]
    list_filter = ["is_compulsory", "is_kcse_subject"]
    search_fields = ["name", "code"]

@admin.register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "school"]