Njuri Senior School
School Management System

🌐 System Overview

A complete digital management system for Njuri Senior School, Kenya.

Covers the school's public website, student records, fee collection, examinations, library, attendance, and parent/student portals  all in one unified platform.

⚙️ Modules
Module	Description
🌐 Public Website	Home, About, Academics, Gallery, KCSE Results, Contact
👩‍🎓 Student Management	Enrollment, profiles, streams, bulk import
💰 Fee Management	Fee structures, payments, balances, receipts
📱 M-Pesa Payments	STK Push via Safaricom Daraja API
📝 Exams & Results	Marks entry, grading, report cards
📚 Library	Books, borrowing, returns, overdue fines
🗓️ Timetable	Class schedules per stream
✅ Attendance	Daily per-stream attendance tracking
📢 Notice Board	School announcements by audience & priority
👨‍👩‍👧 Parent Portal	Fee status, results, notices
🎓 Student Portal	Timetable, results, library
📲 Bulk SMS	Africa's Talking integration
📊 Admin Dashboard	School-wide analytics
👨‍💼 Staff Management	Staff profiles and roles
🚀 System Setup
1. Install
git clone https://github.com/Mbaka-cmd/NJURI-HIGH-SCHOOL.git
cd NJURI-HIGH-SCHOOL
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
2. Environment
cp .env.example .env

Fill in .env:

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
EMAIL_HOST_USER=school-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
AT_USERNAME=africastalking-username
AT_API_KEY=africastalking-api-key
3. Database & First Run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
4. Access Points
Admin panel: /admin/
Student portal: /portal/
Parent portal: /portal/parent/
💳 M-Pesa Setup
Register at https://developer.safaricom.co.ke
Add Consumer Key, Consumer Secret, Shortcode, Passkey to .env
Set callback URL:
https://yourdomain.com/fees/mpesa/callback/
📲 SMS Setup
Register at https://africastalking.com
Add credentials to .env
🔒 Security
Role-based access (Admin, Teacher, Student, Parent)
Secrets stored in .env only
CSRF protection enabled
No sensitive data committed to Git
📞 Technical Support

System: Njuri Senior School Management System
Region: Kenya
Maintainer: Mbaka-cmd
Email: official.mercymbaka@gmail.com
