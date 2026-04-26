Njuri Senior School – School Management System

A full end-to-end digital school management platform built for Njuri Senior School, Kenya.
This system unifies the school website, academic records, financial workflows, parent/student portals, and communication tools into one reliable, secure infrastructure.

🌐 System Overview

This platform digitizes the entire school lifecycle:

Public website
Student information system
Fee management and receipting
Exams + report cards
Library management
Timetable
Attendance
M-Pesa collections (STK Push)
Bulk SMS (Africa’s Talking)
Role-based dashboards for Admin, Teachers, Parents, Students
⚙️ Modules Included
Module	Description
🌐 Public Website	Home, About, Academics, Gallery, KCSE Results, Contact
👩‍🎓 Student Management	Admissions, profiles, streams, bulk import
💰 Fee Management	Structures, payments, balances, digital receipts
📱 M-Pesa STK Push	Safaricom Daraja API integration
📝 Exams & Report Cards	Marks entry, grading, downloadable reports
📚 Library System	Books, borrowing/returning, fines (KES 50/day)
🗓 Timetable	Class schedules per stream
✅ Attendance	Daily tracking per class/stream
📢 Notice Board	Announcements with priority levels
👨‍👩‍👧 Parent Portal	Fees, results, notices
🎓 Student Portal	Results, timetable, library
📲 Bulk SMS	Africa’s Talking messaging
📊 Admin Dashboard	Analytics and school-wide insights
👨‍💼 Staff Management	Staff profiles, roles, permissions
🚀 Installation & Setup
1. Clone the Repository
git clone https://github.com/Mbaka-cmd/NJURI-HIGH-SCHOOL.git
cd NJURI-HIGH-SCHOOL
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
🔧 Environment Configuration

Create your environment file:

cp .env.example .env

Fill in the required keys inside .env:

SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

EMAIL_HOST_USER=school-email@gmail.com
EMAIL_HOST_PASSWORD=app-password

AT_USERNAME=africastalking-username
AT_API_KEY=africastalking-api-key
🗄 Database Setup & First Run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Access Points
Admin Panel → /admin/
Student Portal → /portal/
Parent Portal → /portal/parent/
💳 M-Pesa Daraja Integration
Register on:
https://developer.safaricom.co.ke
Generate:
Consumer Key
Consumer Secret
Shortcode
Passkey
Add them to .env.
Callback URL:
https://yourdomain.com/fees/mpesa/callback/
📲 SMS Integration (Africa’s Talking)
Register at:
https://africastalking.com
Add credentials to .env
System supports bulk SMS for:
Fees reminders
Notices
Academic alerts
🔒 Security Features
Role-based access: Admin, Teacher, Student, Parent
All secrets stored only in .env
CSRF protection enabled
No sensitive files committed to Git
SQLite ignored from Git tracking
📞 Technical Support

System: Njuri Senior School Management System
Region: Kenya
Maintainer: Mbaka-cmd
Email: official.mercymbaka@gmail.com
