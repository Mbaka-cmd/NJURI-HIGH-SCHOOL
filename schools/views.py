from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student, TeacherProfile
from exams.models import Exam
from fees.models import FeeInvoice
from academics.models import Stream


@login_required
def admin_dashboard(request):
    school = request.user.school
    context = {
        "school": school,
        "total_students": Student.objects.filter(school=school, is_active=True).count(),
        "total_teachers": TeacherProfile.objects.filter(school=school, is_active=True).count(),
        "total_streams": Stream.objects.filter(school=school).count(),
        "pending_fees": FeeInvoice.objects.filter(school=school, status="pending").count(),
        "recent_exams": Exam.objects.filter(school=school).order_by("-created_at")[:5],
    }
    return render(request, "schools/admin_dashboard.html", context)