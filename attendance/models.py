from django.db import models
from django.utils import timezone
from students.models import Student
from academics.models import Stream
from schools.models import School


class AttendanceSession(models.Model):
    SESSION_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('full_day', 'Full Day'),
    ]
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='attendance_sessions')
    date = models.DateField(default=timezone.now)
    session = models.CharField(max_length=20, choices=SESSION_CHOICES, default='full_day')
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='attendance_sessions')
    taken_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'session', 'stream')
        ordering = ['-date', 'stream']

    def __str__(self):
        return f"{self.stream} - {self.date} ({self.session})"

    @property
    def total_present(self):
        return self.records.filter(status='present').count()

    @property
    def total_absent(self):
        return self.records.filter(status='absent').count()

    @property
    def total_students(self):
        return self.records.count()


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('session', 'student')
        ordering = ['student__last_name']

    def __str__(self):
        return f"{self.student} - {self.status}"
