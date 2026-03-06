from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TimetableSlot, DAYS, PERIODS
from academics.models import Stream, Subject
from accounts.models import User
from schools.models import AcademicYear, Term
from schools.views import admin_required


BREAK_PERIODS = {'5', '9'}


def build_timetable_grid(slots):
    """Build a day x period grid from slots queryset"""
    grid = {}
    for day, _ in DAYS:
        grid[day] = {}
        for period, _ in PERIODS:
            grid[day][period] = None
    for slot in slots:
        grid[slot.day][slot.period] = slot
    return grid


# ── ADMIN: TIMETABLE LIST ────────────────────────────────────
@admin_required
def timetable_list(request):
    school = request.user.school
    streams = Stream.objects.filter(school=school).order_by(
        'class_level__level_order', 'name'
    )
    years = AcademicYear.objects.filter(school=school)
    terms = Term.objects.filter(academic_year__school=school)

    selected_stream = None
    selected_year = None
    selected_term = None
    grid = None
    days = DAYS
    periods = PERIODS

    stream_id = request.GET.get('stream')
    year_id = request.GET.get('year')
    term_id = request.GET.get('term')

    if stream_id and year_id:
        selected_stream = get_object_or_404(Stream, id=stream_id, school=school)
        selected_year = get_object_or_404(AcademicYear, id=year_id, school=school)
        if term_id:
            selected_term = get_object_or_404(Term, id=term_id)

        slots = TimetableSlot.objects.filter(
            school=school,
            stream=selected_stream,
            academic_year=selected_year,
        ).select_related('subject', 'teacher')

        if selected_term:
            slots = slots.filter(term=selected_term)

        grid = build_timetable_grid(slots)

    context = {
        'streams': streams,
        'years': years,
        'terms': terms,
        'selected_stream': selected_stream,
        'selected_year': selected_year,
        'selected_term': selected_term,
        'grid': grid,
        'days': days,
        'periods': periods,
        'break_periods': BREAK_PERIODS,
    }
    return render(request, 'timetable/timetable_list.html', context)


# ── ADMIN: EDIT TIMETABLE SLOT ───────────────────────────────
@admin_required
def timetable_edit(request, stream_id, year_id):
    school = request.user.school
    stream = get_object_or_404(Stream, id=stream_id, school=school)
    academic_year = get_object_or_404(AcademicYear, id=year_id, school=school)
    subjects = Subject.objects.filter(school=school).order_by('name')
    teachers = User.objects.filter(school=school, is_teacher=True, is_active=True).order_by('last_name')
    terms = Term.objects.filter(academic_year=academic_year)
    term_id = request.GET.get('term') or request.POST.get('term')
    selected_term = None
    if term_id:
        selected_term = Term.objects.filter(id=term_id).first()

    if request.method == 'POST' and 'save_timetable' in request.POST:
        saved = 0
        for day, _ in DAYS:
            for period, _ in PERIODS:
                key = f"{day}_{period}"
                subject_id = request.POST.get(f"subject_{key}")
                teacher_id = request.POST.get(f"teacher_{key}")
                is_break = period in BREAK_PERIODS

                subject = Subject.objects.filter(id=subject_id, school=school).first() if subject_id else None
                teacher = User.objects.filter(id=teacher_id, school=school).first() if teacher_id else None

                TimetableSlot.objects.update_or_create(
                    school=school,
                    stream=stream,
                    academic_year=academic_year,
                    day=day,
                    period=period,
                    defaults={
                        'subject': subject,
                        'teacher': teacher,
                        'is_break': is_break,
                        'term': selected_term,
                    }
                )
                saved += 1

        messages.success(request, f"Timetable saved for {stream.full_name}!")
        url = f"/timetable/edit/{stream_id}/{year_id}/"
        if selected_term:
            url += f"?term={selected_term.id}"
        return redirect(url)

    slots = TimetableSlot.objects.filter(
        school=school, stream=stream, academic_year=academic_year,
    ).select_related('subject', 'teacher')
    if selected_term:
        slots = slots.filter(term=selected_term)

    grid = build_timetable_grid(slots)

    context = {
        'stream': stream,
        'academic_year': academic_year,
        'subjects': subjects,
        'teachers': teachers,
        'terms': terms,
        'selected_term': selected_term,
        'grid': grid,
        'days': DAYS,
        'periods': PERIODS,
        'break_periods': BREAK_PERIODS,
    }
    return render(request, 'timetable/timetable_edit.html', context)


# ── TEACHER: VIEW OWN TIMETABLE ──────────────────────────────
@login_required
def teacher_timetable(request):
    school = request.user.school
    teacher = request.user

    if not (teacher.is_teacher or teacher.is_school_admin):
        return redirect(teacher.get_dashboard_url())

    years = AcademicYear.objects.filter(school=school)
    year_id = request.GET.get('year')
    selected_year = None
    teacher_slots = []

    if year_id:
        selected_year = get_object_or_404(AcademicYear, id=year_id, school=school)
        teacher_slots = TimetableSlot.objects.filter(
            school=school,
            teacher=teacher,
            academic_year=selected_year,
        ).select_related('stream', 'subject').order_by('day', 'period')
    else:
        latest_year = years.order_by('-year').first()
        if latest_year:
            selected_year = latest_year
            teacher_slots = TimetableSlot.objects.filter(
                school=school,
                teacher=teacher,
                academic_year=latest_year,
            ).select_related('stream', 'subject').order_by('day', 'period')

    # Group by day
    schedule = {}
    for day, day_label in DAYS:
        schedule[day] = {
            'label': day_label,
            'slots': [s for s in teacher_slots if s.day == day]
        }

    context = {
        'years': years,
        'selected_year': selected_year,
        'schedule': schedule,
        'days': DAYS,
        'total_lessons': len([s for s in teacher_slots if not s.is_break]),
    }
    return render(request, 'timetable/teacher_timetable.html', context)


# ── STUDENT: VIEW STREAM TIMETABLE ──────────────────────────
@login_required
def student_timetable(request):
    user = request.user
    try:
        student = user.student_profile
        stream = student.current_stream
    except Exception:
        return redirect(user.get_dashboard_url())

    school = user.school
    years = AcademicYear.objects.filter(school=school)
    year_id = request.GET.get('year')
    selected_year = years.order_by('-year').first()

    if year_id:
        selected_year = get_object_or_404(AcademicYear, id=year_id, school=school)

    grid = None
    if stream and selected_year:
        slots = TimetableSlot.objects.filter(
            school=school,
            stream=stream,
            academic_year=selected_year,
        ).select_related('subject', 'teacher')
        grid = build_timetable_grid(slots)

    context = {
        'student': student,
        'stream': stream,
        'years': years,
        'selected_year': selected_year,
        'grid': grid,
        'days': DAYS,
        'periods': PERIODS,
        'break_periods': BREAK_PERIODS,
    }
    return render(request, 'timetable/student_timetable.html', context)