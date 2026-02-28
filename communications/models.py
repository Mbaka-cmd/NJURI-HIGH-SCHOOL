from django.db import models

# Create your models here.
import uuid
from django.db import models

DAYS_OF_WEEK = [
    (1, "Monday"), (2, "Tuesday"), (3, "Wednesday"),
    (4, "Thursday"), (5, "Friday"),
]


class TimetablePeriod(models.Model):
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="timetable_periods")
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    order = models.PositiveSmallIntegerField()
    is_break = models.BooleanField(default=False)

    class Meta:
        unique_together = ("school", "order")
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')}–{self.end_time.strftime('%H:%M')})"


class Timetable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="timetable_entries")
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.CASCADE)
    term = models.ForeignKey("schools.Term", on_delete=models.CASCADE, related_name="timetable_entries")
    stream = models.ForeignKey("academics.Stream", on_delete=models.CASCADE, related_name="timetable_entries")
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    period = models.ForeignKey(TimetablePeriod, on_delete=models.CASCADE)
    subject = models.ForeignKey("academics.Subject", on_delete=models.CASCADE)
    teacher = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="timetable_lessons")
    room = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("stream", "day_of_week", "period", "academic_year", "term")
        ordering = ["day_of_week", "period__order"]

    def __str__(self):
        return f"{self.stream} — {self.get_day_of_week_display()} {self.period} — {self.subject}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="sent_messages")
    recipients = models.ManyToManyField("accounts.User", through="MessageRecipient", related_name="received_messages")
    subject = models.CharField(max_length=300)
    body = models.TextField()
    message_type = models.CharField(
        max_length=20,
        choices=[
            ("direct", "Direct Message"), ("announcement", "Announcement"),
            ("alert", "Urgent Alert"), ("fee_reminder", "Fee Reminder"),
            ("result_notification", "Results Ready"),
        ],
        default="direct",
    )
    target_stream = models.ForeignKey("academics.Stream", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="stream_messages")
    target_role = models.CharField(max_length=20, blank=True,
        choices=[("all", "All"), ("parents", "All Parents"), ("teachers", "All Teachers")])
    is_sms = models.BooleanField(default=False)
    is_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"From {self.sender} — {self.subject[:50]}"


class MessageRecipient(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("message", "recipient")


class ParentComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="parent_comments")
    author_name = models.CharField(max_length=200)
    author_email = models.EmailField(blank=True)
    author_phone = models.CharField(max_length=20, blank=True)
    author_user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="public_comments")
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True,
        choices=[(1,"⭐"),(2,"⭐⭐"),(3,"⭐⭐⭐"),(4,"⭐⭐⭐⭐"),(5,"⭐⭐⭐⭐⭐")])
    category = models.CharField(max_length=30,
        choices=[
            ("general", "General Feedback"), ("academics", "Academic Excellence"),
            ("facilities", "Facilities"), ("staff", "Staff & Teaching"),
            ("co_curricular", "Co-curricular"),
        ],
        default="general",
    )
    status = models.CharField(max_length=20,
        choices=[
            ("pending", "Pending Review"), ("approved", "Approved"),
            ("rejected", "Rejected"), ("flagged", "Flagged"),
        ],
        default="pending",
    )
    moderated_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="moderated_comments")
    moderation_note = models.TextField(blank=True)
    moderated_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "display_order", "-submitted_at"]

    def __str__(self):
        return f"{self.author_name} — {self.status}"