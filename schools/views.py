from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from students.models import Student
from exams.models import Exam, ExamResult, ReportCard, score_to_grade
from fees.models import FeeInvoice
from academics.models import Stream, Subject
from accounts.models import User
import json


@login_required
def admin_dashboard(request):
    school = request.user.school

    total_students = Student.objects.filter(school=school, is_active=True).count()
    total_teachers = User.objects.filter(school=school, is_teacher=True, is_active=True).count()
    total_streams = Stream.objects.filter(school=school).count()
    total_subjects = Subject.objects.filter(school=school).count()
    total_exams = Exam.objects.filter(school=school).count()

    all_invoices = FeeInvoice.objects.filter(school=school)
    total_expected = all_invoices.aggregate(t=Sum('total_expected'))['t'] or 0
    total_collected = all_invoices.aggregate(t=Sum('total_paid'))['t'] or 0
    total_balance = total_expected - total_collected
    collection_rate = round((total_collected / total_expected * 100), 1) if total_expected > 0 else 0

    streams = Stream.objects.filter(school=school).order_by('class_level__level_order', 'name')
    stream_labels = [s.full_name for s in streams]
    stream_counts = [s.students.filter(is_active=True).count() for s in streams]

    paid_count = all_invoices.filter(status='paid').count()
    pending_count = all_invoices.filter(status='pending').count()
    partial_count = all_invoices.filter(status='partial').count()
    overdue_count = all_invoices.filter(status='overdue').count()

    grade_labels = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'E']
    grade_counts = [ExamResult.objects.filter(exam__school=school, grade=g).count() for g in grade_labels]

    recent_exams = Exam.objects.filter(school=school).order_by('-created_at')[:5]
    recent_students = Student.objects.filter(school=school, is_active=True).order_by('-created_at')[:5]

    context = {
        "school": school,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_streams": total_streams,
        "total_subjects": total_subjects,
        "total_exams": total_exams,
        "total_expected": total_expected,
        "total_collected": total_collected,
        "total_balance": total_balance,
        "collection_rate": collection_rate,
        "stream_labels": json.dumps(stream_labels),
        "stream_counts": json.dumps(stream_counts),
        "fee_data": json.dumps([paid_count, pending_count, partial_count, overdue_count]),
        "grade_labels": json.dumps(grade_labels),
        "grade_counts": json.dumps(grade_counts),
        "recent_exams": recent_exams,
        "recent_students": recent_students,
    }
    return render(request, "schools/admin_dashboard.html", context)