from django.db import models

# Create your models here.
import uuid
from django.db import models


class SubjectCategory(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="subject_categories")

    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="subjects")
    category = models.ForeignKey(SubjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20)
    is_compulsory = models.BooleanField(default=False)
    is_kcse_subject = models.BooleanField(default=True)
    max_score = models.PositiveSmallIntegerField(default=100)
    kcse_points_weight = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)

    class Meta:
        unique_together = ("school", "code")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class ClassLevel(models.Model):
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="class_levels")
    name = models.CharField(max_length=50)
    level_order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("school", "level_order")
        ordering = ["level_order"]

    def __str__(self):
        return f"{self.school.name} — {self.name}"


class Stream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="streams")
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name="streams")
    name = models.CharField(max_length=50)
    class_teacher = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="class_teacher_streams",
    )
    subjects = models.ManyToManyField(Subject, through="StreamSubject", related_name="streams")
    capacity = models.PositiveSmallIntegerField(default=45)

    class Meta:
        unique_together = ("class_level", "name")
        ordering = ["class_level__level_order", "name"]

    def __str__(self):
        return f"{self.class_level.name} {self.name}"

    @property
    def full_name(self):
        return f"{self.class_level.name} {self.name}"

    @property
    def student_count(self):
        return self.students.filter(is_active=True).count()


class StreamSubject(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="teaching_assignments",
    )
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("stream", "subject", "academic_year")

    def __str__(self):
        return f"{self.stream} — {self.subject}"