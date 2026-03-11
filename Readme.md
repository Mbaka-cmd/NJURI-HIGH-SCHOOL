# 🏫 St. Bakhita Chuka Girls High School
### School Management System

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Django](https://img.shields.io/badge/Django-5.1-green) ![M-Pesa](https://img.shields.io/badge/Payments-M--Pesa-brightgreen)

---

## 🌐 System Overview

A complete digital management system for St. Bakhita Chuka Girls High School, Chuka — Tharaka-Nithi County.

Covers the school's public website, student records, fee collection, examinations, library, attendance, and parent/student portals — all in one platform.

---

## ⚙️ Modules

| Module | Description |
|--------|-------------|
| 🌐 Public Website | Home, About, Academics, Gallery, KCSE Results, Contact |
| 👩‍🎓 Student Management | Enrollment, profiles, streams, bulk import |
| 💰 Fee Management | Fee structures, payments, balances, receipts |
| 📱 M-Pesa Payments | STK Push via Safaricom Daraja API |
| 📝 Exams & Results | Marks entry, grading, report cards |
| 📚 Library | Books, borrowing, returns, overdue fines |
| 🗓️ Timetable | Class schedules per stream |
| ✅ Attendance | Daily per-stream attendance tracking |
| 📢 Notice Board | School announcements by audience & priority |
| 👨‍👩‍👧 Parent Portal | Fee status, results, notices |
| 🎓 Student Portal | Timetable, results, library |
| 📲 Bulk SMS | Africa's Talking integration |
| 📊 Admin Dashboard | School-wide analytics |
| 👨‍💼 Staff Management | Staff profiles and roles |

---

## 🚀 System Setup

### 1. Install
```bash
git clone https://github.com/Mbaka-cmd/SCHOOL-MANAGEMENT-SYSTEM-FINAL.git
cd SCHOOL-MANAGEMENT-SYSTEM-FINAL
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment
```bash
cp .env.example .env
```
Fill in `.env` with school credentials:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
EMAIL_HOST_USER=school-email@gmail.com
EMAIL_HOST_PASSWORD=app-password
AT_USERNAME=africastalking-username
AT_API_KEY=africastalking-api-key
```

### 3. Database & First Run
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 4. Access Points
- Admin panel: `/admin/`
- Student portal: `/portal/`
- Parent portal: `/portal/parent/`

---

## 💳 M-Pesa Setup

1. Register at [developer.safaricom.co.ke](https://developer.safaricom.co.ke)
2. Add Consumer Key, Consumer Secret, Shortcode, Passkey to `.env`
3. Set callback URL: `https://yourdomain.com/fees/mpesa/callback/`

---

## 📲 SMS Setup

1. Register at [africastalking.com](https://africastalking.com)
2. Add `AT_USERNAME` and `AT_API_KEY` to `.env`

---

## 🔒 Security

- Role-based access — Admin, Teacher, Student, Parent
- All secrets in `.env` — never committed to git
- CSRF protection on all forms
- Student data excluded from version control

---

## 📞 Technical Support

**Developer:** Mercy Kathomi Mbaka
**Email:** official.mercymbaka@gmail.com