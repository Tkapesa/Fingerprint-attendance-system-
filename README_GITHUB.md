# 🔐 Fingerprint Attendance System

A Django-based fingerprint attendance management system using the R307 optical fingerprint sensor. This system allows students to mark attendance by scanning their fingerprints, and instructors to view and manage attendance records through an intuitive dashboard.

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Features

### For Students
- ✅ **Self-Registration**: Students can register with email, password, full name, student ID, and course selection
- 👆 **Fingerprint Enrollment**: Easy fingerprint enrollment process after registration
- 📝 **Quick Attendance**: Mark attendance by simply scanning fingerprint (no login required)
- 📊 **View Profile**: Access personal profile and attendance history
- 🔒 **Duplicate Prevention**: Cannot mark attendance twice for the same course on the same day

### For Instructors/Admins
- 📚 **Course Management**: Create and manage courses with course codes
- 👥 **Student Management**: View all registered students and their details
- 📈 **Attendance Dashboard**: Real-time overview of all courses and attendance statistics
- 🔍 **Detailed Reports**: View detailed attendance for each course with date filtering
- 📊 **Excel Export**: Download attendance reports in Excel format
- 🎯 **Course-Based Viewing**: Filter attendance by course code

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- R307 Fingerprint Sensor (optional for testing)
- pip package manager
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Tkapesa/Fingerprint-attendance-system-.git
cd Fingerprint-attendance-system-
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# OR
.venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create admin account**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Home: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- Student Registration: http://127.0.0.1:8000/register/

## 📖 Usage Guide

### Initial Setup

1. **Login to Admin Panel** (http://127.0.0.1:8000/admin/)
2. **Create Courses**:
   - Navigate to "Courses" under USERS section
   - Click "Add Course"
   - Enter Course Code (e.g., CS101), Course Name, and Instructor name
   - Save the course

### Student Workflow

1. **Register**: Go to `/register/` and fill in details
   - Full Name
   - Email Address
   - Student ID
   - Select Course from dropdown
   - Create Password

2. **Enroll Fingerprint**: After registration, you'll be redirected to enrollment page
   - Click "Start Fingerprint Enrollment"
   - Follow the prompts to enroll your fingerprint

3. **Mark Attendance**: Go to `/fingerprint/scan/`
   - No login required!
   - Click "Scan Fingerprint for Attendance"
   - Place finger on sensor
   - Attendance recorded automatically with timestamp

### Instructor Workflow

1. **Login**: Use your admin credentials at `/login/`

2. **View Dashboard**: Navigate to `/attendance/dashboard/`
   - See all courses
   - View today's attendance statistics
   - Total enrolled students per course

3. **View Course Details**: Click "View Attendance" on any course
   - See list of all students who attended
   - Filter by date range
   - Download Excel report

## 🏗️ System Architecture

```
fingerprint_attendance/          # Main Django project
├── attendance/                  # Attendance tracking app
│   ├── models.py               # AttendanceLog model
│   ├── views.py                # Dashboard & reports
│   └── templates/              # Dashboard templates
│
├── fingerprint/                 # Fingerprint management
│   ├── models.py               # FingerprintScan model
│   ├── views.py                # Enrollment & scanning
│   ├── r307.py                 # R307 sensor interface
│   └── templates/              # Enrollment/scan templates
│
├── users/                       # User management
│   ├── models.py               # Course & UserProfile models
│   ├── views.py                # Registration & login
│   └── templates/              # Auth templates
│
└── reports/                     # Future reporting features
```

## 📊 Database Models

### Course
- `course_code` (Primary Key, unique)
- `course_name`
- `instructor`

### UserProfile
- `user` (One-to-One with Django User)
- `full_name`
- `email`
- `student_id` (unique)
- `course` (Foreign Key to Course)
- `role` (instructor/student)
- `fingerprint_template`
- `fingerprint_enrolled`

### AttendanceLog
- `user` (Foreign Key to User)
- `student_name` (denormalized)
- `student_id` (denormalized)
- `course` (Foreign Key to Course)
- `timestamp`
- `date`
- `time`
- `status` (present/absent)
- `scan_method`

**Constraint**: Unique together on [user, course, date] - prevents duplicate attendance

## 🔧 Configuration

### R307 Sensor Setup

1. Connect R307 sensor via USB to serial adapter
2. Identify the serial port (e.g., `/dev/ttyUSB0` on Linux, `COM3` on Windows)
3. Update `fingerprint/r307.py` with correct port:
```python
SERIAL_PORT = '/dev/ttyUSB0'  # Change to your port
```

### Development vs Production

**Development** (current setup):
- Uses simulated fingerprint data
- SQLite database
- DEBUG = True

**Production** (recommended):
- Connect real R307 sensor
- Use PostgreSQL database
- Set DEBUG = False
- Configure ALLOWED_HOSTS
- Use Gunicorn/uWSGI
- Enable HTTPS

## 📁 Key Files

- `COMPLETE_SETUP_GUIDE.txt` - Detailed setup instructions
- `TESTING_GUIDE.md` - Step-by-step testing procedures
- `DEPLOYMENT_CHECKLIST.txt` - Production deployment guide
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules (excludes venv, db, cache)

## 🛠️ Technologies Used

- **Backend**: Django 5.2
- **Database**: SQLite (development), PostgreSQL recommended (production)
- **Hardware**: R307 Optical Fingerprint Sensor
- **Python Libraries**:
  - `pyserial` - Serial communication with sensor
  - `pandas` - Data processing
  - `openpyxl` - Excel report generation
- **Frontend**: HTML, CSS (embedded in templates)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Tkapesa**
- GitHub: [@Tkapesa](https://github.com/Tkapesa)
- Repository: [Fingerprint-attendance-system-](https://github.com/Tkapesa/Fingerprint-attendance-system-.git)

## 🙏 Acknowledgments

- Django Documentation
- R307 Fingerprint Sensor Community
- Python Serial Communication Libraries

## 📞 Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

---

**Note**: This system is currently configured for development/testing with simulated fingerprint data. For production use with real R307 sensor, update the `fingerprint/r307.py` file with your hardware configuration.

**Happy Coding! 🚀**
