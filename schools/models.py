from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.utils.text import slugify


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    motto = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to="schools/logos/", null=True, blank=True)

    # Contact
    address = models.TextField()
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    po_box = models.CharField(max_length=50, blank=True)

    # Academic Identity
    knec_code = models.CharField(max_length=20, blank=True)
    school_type = models.CharField(
        max_length=20,
        choices=[("boarding", "Boarding"), ("day", "Day"), ("mixed", "Day & Boarding")],
        default="mixed",
    )
    gender_type = models.CharField(
        max_length=10,
        choices=[("girls", "Girls"), ("boys", "Boys"), ("mixed", "Mixed")],
        default="girls",
    )
    category = models.CharField(
        max_length=20,
        choices=[
            ("national", "National"),
            ("extra_county", "Extra County"),
            ("county", "County"),
            ("sub_county", "Sub County"),
        ],
        default="county",
    )

    # SaaS Subscription
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ("trial", "Free Trial"),
            ("basic", "Basic"),
            ("premium", "Premium"),
            ("enterprise", "Enterprise"),
        ],
        default="trial",
    )
    subscription_expires = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Current Academic Context
    current_year = models.PositiveIntegerField(null=True, blank=True)
    current_term = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AcademicYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="academic_years")
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ("school", "year")
        ordering = ["-year"]

    def __str__(self):
        return f"{self.school.name} — {self.year}"

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.filter(school=self.school, is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class Term(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="terms")
    number = models.PositiveSmallIntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")])
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ("academic_year", "number")
        ordering = ["number"]

    def __str__(self):
        return f"{self.academic_year.year} — Term {self.number}"