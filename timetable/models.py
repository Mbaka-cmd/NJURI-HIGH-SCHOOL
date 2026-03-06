import uuid
from django.db import models

DAYS = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
]

PERIODS = [
    ('1', 'Period 1 (7:00 - 7:40)'),
    ('2', 'Period 2 (7:40 - 8:20)'),
    ('3', 'Period 3 (8:20 - 9:00)'),
    ('4', 'Period 4 (9:00 - 9:40)'),
    ('5', 'Break (9:40 - 10:00)'),
    ('6', 'Period 5 (10:00 - 10:40)'),
    ('7', 'Period 6 (10:40 - 11:20)'),
    ('8', 'Period 7 (11:20 - 12:00)'),
    ('9', 'Lunch (12:00 - 1:00)'),
    ('10', 'Period 8 (1:00 - 1:40)'),
    ('11', 'Period 9 (1:40 - 2:20)'),
    ('12', 'Period 10 (2:20 - 3:00)'),
]


class TimetableSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='timetable_slots')
    stream = models.ForeignKey('academics.Stream', on_delete=models.CASCADE, related_name='timetable_slots')
    academic_year = models.ForeignKey('schools.AcademicYear', on_delete=models.CASCADE, related_name='timetable_slots')
    term = models.ForeignKey('schools.Term', on_delete=models.CASCADE, related_name='timetable_slots', null=True, blank=True)
    day = models.CharField(max_length=10, choices=DAYS)
    period = models.CharField(max_length=5, choices=PERIODS)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_slots')
    is_break = models.BooleanField(default=False)
    notes = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('stream', 'academic_year', 'day', 'period')
        ordering = ['day', 'period']

    def __str__(self):
        return f"{self.stream} - {self.get_day_display()} P{self.period} - {self.subject}"

    def get_period_time(self):
        period_times = {
            '1': '7:00-7:40', '2': '7:40-8:20', '3': '8:20-9:00',
            '4': '9:00-9:40', '5': 'BREAK', '6': '10:00-10:40',
            '7': '10:40-11:20', '8': '11:20-12:00', '9': 'LUNCH',
            '10': '1:00-1:40', '11': '1:40-2:20', '12': '2:20-3:00',
        }
        return period_times.get(self.period, '')