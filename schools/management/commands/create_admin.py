from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
 
User = get_user_model()
 
SCHOOL_NAME = "Njuri Senior School"
SCHOOL_SLUG = "njuri-senior-school"
SCHOOL_MOTTO = "Knowledge, Discipline and Service"
SCHOOL_EMAIL = "njurihschool@yahoo.com"
SCHOOL_PHONE = "0722454131"
SCHOOL_ADDRESS = "Magumoni Location, Meru South Sub-County, Tharaka-Nithi County"
SCHOOL_COUNTY = "Tharaka-Nithi"
SCHOOL_KNEC = "19308504"
SCHOOL_CATEGORY = "extra_county"
SCHOOL_TYPE = "boarding"
SCHOOL_GENDER = "mixed"
 
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "official.mercymbaka@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "MercyAdmin2026!")
 
KCSE_DATA = [
    {
        "year": 2024, "candidates": 180, "mean_grade": "C+",
        "grade_a_plain": 0, "grade_a_minus": 2, "grade_b_plus": 8,
        "grade_b_plain": 18, "grade_b_minus": 32, "grade_c_plus": 45,
        "grade_c_plain": 38, "grade_c_minus": 22, "grade_d_plus": 10,
        "grade_d_plain": 4, "grade_d_minus": 1, "grade_e": 0, "is_published": True,
    },
    {
        "year": 2023, "candidates": 175, "mean_grade": "C+",
        "grade_a_plain": 0, "grade_a_minus": 1, "grade_b_plus": 6,
        "grade_b_plain": 15, "grade_b_minus": 28, "grade_c_plus": 44,
        "grade_c_plain": 40, "grade_c_minus": 25, "grade_d_plus": 12,
        "grade_d_plain": 3, "grade_d_minus": 1, "grade_e": 0, "is_published": True,
    },
    {
        "year": 2013, "candidates": 150, "mean_grade": "B",
        "grade_a_plain": 0, "grade_a_minus": 3, "grade_b_plus": 12,
        "grade_b_plain": 28, "grade_b_minus": 35, "grade_c_plus": 30,
        "grade_c_plain": 22, "grade_c_minus": 12, "grade_d_plus": 6,
        "grade_d_plain": 2, "grade_d_minus": 0, "grade_e": 0, "is_published": True,
    },
]
 
STREAMS = [
    ("Form 1", "North"), ("Form 1", "South"), ("Form 1", "East"), ("Form 1", "West"),
    ("Form 2", "North"), ("Form 2", "South"), ("Form 2", "East"), ("Form 2", "West"),
    ("Form 3", "North"), ("Form 3", "South"), ("Form 3", "East"), ("Form 3", "West"),
    ("Form 4", "North"), ("Form 4", "South"), ("Form 4", "East"), ("Form 4", "West"),
]
 
 
class Command(BaseCommand):
    help = "Seed Njuri Senior School data"
 
    def handle(self, *args, **kwargs):
        self._create_admin()
        self._create_school()
        self._create_academic_year()
        self._create_streams()
        self._create_kcse()
 
    def _create_admin(self):
        if User.objects.filter(email=ADMIN_EMAIL).exists():
            self.stdout.write("Admin already exists.")
            return
        User.objects.create_superuser(
            email=ADMIN_EMAIL, password=ADMIN_PASSWORD,
            first_name="Mercy", last_name="Mbaka",
            is_platform_admin=True, is_school_admin=True,
        )
        self.stdout.write(self.style.SUCCESS("Admin created."))
 
    def _create_school(self):
        from schools.models import School
        if School.objects.filter(slug=SCHOOL_SLUG).exists():
            self.stdout.write("School already exists.")
            return
        school = School.objects.create(
            name=SCHOOL_NAME, slug=SCHOOL_SLUG, motto=SCHOOL_MOTTO,
            email=SCHOOL_EMAIL, phone=SCHOOL_PHONE, address=SCHOOL_ADDRESS,
            county=SCHOOL_COUNTY, knec_code=SCHOOL_KNEC,
            category=SCHOOL_CATEGORY, school_type=SCHOOL_TYPE,
            gender_type=SCHOOL_GENDER, is_active=True,
        )
        # Link admin to school
        admin = User.objects.filter(email=ADMIN_EMAIL).first()
        if admin:
            admin.school = school
            admin.save()
        self.stdout.write(self.style.SUCCESS("School created."))
 
    def _create_academic_year(self):
        from schools.models import School, AcademicYear, Term
        school = School.objects.get(slug=SCHOOL_SLUG)
        year, _ = AcademicYear.objects.get_or_create(
            school=school, year=2026, defaults={"is_current": True}
        )
        terms = [
            {"name": "Term 1", "order": 1, "start_date": "2026-01-06", "end_date": "2026-04-03", "is_current": False},
            {"name": "Term 2", "order": 2, "start_date": "2026-05-05", "end_date": "2026-07-31", "is_current": True},
            {"name": "Term 3", "order": 3, "start_date": "2026-09-01", "end_date": "2026-11-06", "is_current": False},
        ]
        for t in terms:
            Term.objects.get_or_create(academic_year=year, name=t["name"], defaults=t)
        self.stdout.write(self.style.SUCCESS("Academic year and terms ready."))
 
    def _create_streams(self):
        from schools.models import School, Stream
        from academics.models import ClassLevel
        school = School.objects.get(slug=SCHOOL_SLUG)
        if Stream.objects.filter(school=school).exists():
            self.stdout.write("Streams already exist.")
            return
        for class_name, stream_name in STREAMS:
            cl, _ = ClassLevel.objects.get_or_create(school=school, name=class_name)
            Stream.objects.get_or_create(school=school, class_level=cl, name=stream_name, defaults={"capacity": 45})
        self.stdout.write(self.style.SUCCESS("Streams created."))
 
    def _create_kcse(self):
        from schools.models import School
        from website.models import KCSEResult
        school = School.objects.get(slug=SCHOOL_SLUG)
        if KCSEResult.objects.filter(school=school).exists():
            self.stdout.write("KCSE results already exist.")
            return
        for r in KCSE_DATA:
            KCSEResult.objects.create(school=school, **r)
        self.stdout.write(self.style.SUCCESS("KCSE results seeded."))