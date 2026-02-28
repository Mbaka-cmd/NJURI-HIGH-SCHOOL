from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TeacherProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="teacher_profile")
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="teachers")
    tsc_number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    employee_number = models.CharField(max_length=30, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    specialization = models.ManyToManyField("academics.Subject", blank=True, related_name="specialist_teachers")
    employment_type = models.CharField(
        max_length=20,
        choices=[
            ("permanent", "Permanent"),
            ("contract", "Contract"),
            ("bom", "BOM (Board of Management)"),
            ("intern", "Teaching Practice"),
        ],
        default="permanent",
    )
    date_joined = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deputy_principal = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    hod_department = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"Teacher: {self.user.get_full_name()}"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="student_profile",
    )
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="students")

    # Identity
    admission_number = models.CharField(max_length=30)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[("female", "Female"), ("male", "Male")],
        default="female",
    )
    profile_photo = models.ImageField(upload_to="students/photos/", null=True, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    birth_certificate_no = models.CharField(max_length=30, blank=True)
    nemis_number = models.CharField(max_length=30, blank=True)

    # Academic Placement
    current_stream = models.ForeignKey(
        "academics.Stream", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="students",
    )
    kcpe_marks = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(500)],
    )
    kcpe_year = models.PositiveSmallIntegerField(null=True, blank=True)
    kcpe_index_number = models.CharField(max_length=30, blank=True)

    # Admission
    admission_date = models.DateField()
    admission_year = models.ForeignKey(
        "schools.AcademicYear", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="admitted_students",
    )
    admission_type = models.CharField(
        max_length=20,
        choices=[
            ("form1", "Form 1 (New)"),
            ("transfer", "Transfer Student"),
            ("repeat", "Repeat Student"),
        ],
        default="form1",
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("graduated", "Graduated"),
            ("transferred", "Transferred Out"),
            ("expelled", "Expelled"),
            ("suspended", "Suspended"),
            ("deceased", "Deceased"),
        ],
        default="active",
    )
    is_active = models.BooleanField(default=True)

    # Boarding
    is_boarder = models.BooleanField(default=True)
    dormitory = models.CharField(max_length=100, blank=True)
    bed_number = models.CharField(max_length=20, blank=True)

    # Medical
    blood_group = models.CharField(
        max_length=5, blank=True,
        choices=[("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),
                 ("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-")]
    )
    medical_conditions = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("school", "admission_number")
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.admission_number})"

    def get_full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p).strip()


class ParentGuardian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="parent_profile",
    )
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="parents")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, blank=True)
    phone_primary = models.CharField(max_length=20)
    phone_secondary = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    relationship = models.CharField(
        max_length=30,
        choices=[
            ("father", "Father"),
            ("mother", "Mother"),
            ("guardian", "Guardian"),
            ("sibling", "Sibling"),
            ("other", "Other"),
        ],
        default="guardian",
    )
    students = models.ManyToManyField(Student, related_name="parents", blank=True)
    is_primary_contact = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.relationship})"


class StudentStreamHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="stream_history")
    stream = models.ForeignKey("academics.Stream", on_delete=models.CASCADE)
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.CASCADE)
    position_in_class = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "academic_year")
        ordering = ["-academic_year__year"]

    def __str__(self):
        return f"{self.student} — {self.stream} ({self.academic_year.year})"