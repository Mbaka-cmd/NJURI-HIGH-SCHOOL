from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student, ParentGuardian
from exams.models import ReportCard, ExamResult, Exam
from fees.models import FeeInvoice
from academics.models import Stream


def portal_redirect(request):
    """Smart redirect based on user role after login."""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_school_admin or request.user.is_teacher:
        return redirect('admin_dashboard')
    if request.user.is_student:
        return redirect('student_dashboard')
    if request.user.is_parent:
        return redirect('parent_dashboard')
    return redirect('home')


@login_required
def student_dashboard(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        messages.error(request, "No student profile linked to your account.")
        return redirect('home')

    school = student.school
    fee_invoices = FeeInvoice.objects.filter(student=student, school=school)
    total_expected = sum(float(inv.total_expected) for inv in fee_invoices)
    total_paid = sum(float(inv.total_paid) for inv in fee_invoices)
    fee_balance = total_expected - total_paid

    report_cards = ReportCard.objects.filter(
        student=student
    ).select_related('exam', 'stream').order_by('-exam__created_at')[:5]

    recent_results = ExamResult.objects.filter(
        student=student
    ).select_related('exam', 'subject').order_by('-exam__created_at')[:10]

    context = {
        'student': student,
        'school': school,
        'fee_invoices': fee_invoices,
        'total_expected': total_expected,
        'total_paid': total_paid,
        'fee_balance': fee_balance,
        'report_cards': report_cards,
        'recent_results': recent_results,
    }
    return render(request, 'portal/student_dashboard.html', context)


@login_required
def student_results(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        return redirect('home')

    exams = Exam.objects.filter(
        school=student.school,
        streams=student.current_stream
    ).order_by('-created_at')

    selected_exam_id = request.GET.get('exam')
    selected_exam = None
    results = []

    if selected_exam_id:
        selected_exam = get_object_or_404(Exam, id=selected_exam_id)
        results = ExamResult.objects.filter(
            exam=selected_exam, student=student
        ).select_related('subject').order_by('subject__name')

    context = {
        'student': student,
        'school': student.school,
        'exams': exams,
        'selected_exam': selected_exam,
        'results': results,
    }
    return render(request, 'portal/student_results.html', context)


@login_required
def student_fees(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        return redirect('home')

    fee_invoices = FeeInvoice.objects.filter(
        student=student, school=student.school
    ).order_by('-created_at')

    context = {
        'student': student,
        'school': student.school,
        'fee_invoices': fee_invoices,
    }
    return render(request, 'portal/student_fees.html', context)


@login_required
def parent_dashboard(request):
    user = request.user
    try:
        parent = ParentGuardian.objects.get(user=user)
    except ParentGuardian.DoesNotExist:
        messages.error(request, "No parent profile linked to your account.")
        return redirect('home')

    students = parent.students.filter(is_active=True).select_related(
        'current_stream', 'school'
    )

    students_data = []
    for student in students:
        school = student.school
        fee_invoices = FeeInvoice.objects.filter(student=student, school=school)
        total_expected = sum(float(inv.total_expected) for inv in fee_invoices)
        total_paid = sum(float(inv.total_paid) for inv in fee_invoices)
        fee_balance = total_expected - total_paid

        latest_report = ReportCard.objects.filter(
            student=student
        ).order_by('-exam__created_at').first()

        students_data.append({
            'student': student,
            'fee_balance': fee_balance,
            'total_paid': total_paid,
            'latest_report': latest_report,
        })

    context = {
        'parent': parent,
        'school': students.first().school if students else None,
        'students_data': students_data,
    }
    return render(request, 'portal/parent_dashboard.html', context)


@login_required
def parent_student_detail(request, student_id):
    user = request.user
    try:
        parent = ParentGuardian.objects.get(user=user)
    except ParentGuardian.DoesNotExist:
        return redirect('home')

    student = get_object_or_404(
        parent.students, id=student_id, is_active=True
    )
    school = student.school

    fee_invoices = FeeInvoice.objects.filter(student=student, school=school)
    total_expected = sum(float(inv.total_expected) for inv in fee_invoices)
    total_paid = sum(float(inv.total_paid) for inv in fee_invoices)
    fee_balance = total_expected - total_paid

    report_cards = ReportCard.objects.filter(
        student=student
    ).select_related('exam').order_by('-exam__created_at')

    context = {
        'parent': parent,
        'student': student,
        'school': school,
        'fee_invoices': fee_invoices,
        'total_expected': total_expected,
        'total_paid': total_paid,
        'fee_balance': fee_balance,
        'report_cards': report_cards,
    }
    return render(request, 'portal/parent_student_detail.html', context)