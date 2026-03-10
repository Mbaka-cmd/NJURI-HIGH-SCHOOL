from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord

class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['stream', 'date', 'session', 'total_present', 'total_absent', 'taken_by']
    list_filter = ['date', 'session', 'stream']
    inlines = [AttendanceRecordInline]

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'remarks']
    list_filter = ['status', 'session__date']
