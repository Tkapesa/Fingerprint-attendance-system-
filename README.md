# 🔐 Fingerprint Attendance System

A Django-based attendance management system using R307 optical fingerprint sensor for automated, secure attendance tracking.

---

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Admin Panel](#admin-panel)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Fingerprint Enrollment**: Register user fingerprints using R307 sensor
- **Automated Attendance**: Mark attendance by fingerprint scanning
- **User Management**: Admin panel for managing users and profiles
- **Excel Reports**: Export attendance data to Excel (.xlsx) format
- **Audit Trail**: Track all scan attempts and attendance logs
- **Manual Override**: Fallback manual attendance logging option
- **Secure Authentication**: Django's built-in user authentication
- **SQLite Database**: Easy-to-deploy, file-based database

---

## 💻 System Requirements

### Software
- **Python**: 3.10 or higher
- **pip**: Python package manager
- **Operating System**: macOS, Linux, or Windows

### Hardware
- **R307 Optical Fingerprint Sensor**
- **USB-to-Serial Adapter** (if sensor doesn't have built-in USB)
- **Computer** with available USB port

---

## 📦 Installation

### Step 1: Clone or Download Project

```bash
cd /path/to/project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- Django 5.2+ (Web framework)
- pandas 2.2.3+ (Data processing)
- openpyxl 3.1.5+ (Excel export)
- pyserial 3.5+ (Sensor communication)

### Step 4: Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Admin User

```bash
python manage.py createsuperuser
```

Follow prompts to create admin credentials:
- Username: (your choice)
- Email: (optional)
- Password: (secure password)

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Access the application at: **http://127.0.0.1:8000**

---

## 🔌 Hardware Setup

### R307 Sensor Connection

1. **Connect Sensor to Computer**
   - Plug R307 sensor into USB port (via USB-to-Serial adapter if needed)

2. **Find Serial Port**

   **macOS/Linux:**
   ```bash
   ls /dev/tty.*
   # Look for: /dev/tty.usbserial-XXXXX or /dev/ttyUSB0
   ```

   **Windows:**
   - Open Device Manager
   - Look under "Ports (COM & LPT)"
   - Note the COM port (e.g., COM3)

3. **Update Configuration**
   
   Edit `fingerprint/r307.py`:
   ```python
   SERIAL_PORT = '/dev/tty.usbserial-XXXXX'  # macOS/Linux
   # OR
   SERIAL_PORT = 'COM3'  # Windows
   ```

4. **Test Connection**
   - Try enrolling a fingerprint
   - Check console for connection messages

---

## 🚀 Usage

### For Administrators

#### 1. Access Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Login with superuser credentials
- Manage users, profiles, attendance logs

#### 2. Create User Profiles
- Go to Admin Panel → Users → Add User
- Create username and password
- Go to User Profiles → Add User Profile
- Select user and set role (Admin/Student)

#### 3. Enroll Fingerprints
- URL: http://127.0.0.1:8000/fingerprint/enroll/
- Enter username
- Click "Start Enrollment"
- User places finger on sensor
- Wait for confirmation

#### 4. Generate Reports
- URL: http://127.0.0.1:8000/reports/generate/
- Excel file downloads automatically
- Contains all attendance records

### For Students/Users

#### 1. Mark Attendance
- URL: http://127.0.0.1:8000/fingerprint/scan/
- Click "Scan Now"
- Place enrolled finger on sensor
- Attendance marked automatically

#### 2. Manual Attendance (Fallback)
- URL: http://127.0.0.1:8000/attendance/log/
- Use when sensor is unavailable
- Requires login

---

## 📁 Project Structure

```
fingerprint_attendance/          # Main Django project
├── settings.py                  # Project configuration
├── urls.py                      # Main URL routing
└── views.py                     # Home page view

users/                           # User management app
├── models.py                    # UserProfile model
└── admin.py                     # Admin configuration

fingerprint/                     # Fingerprint functionality
├── models.py                    # FingerprintScan model
├── views.py                     # Enroll/scan views
├── urls.py                      # Fingerprint URLs
├── r307.py                      # Sensor interface
└── templates/fingerprint/
    ├── enroll.html             # Enrollment page
    └── scan.html               # Scanning page

attendance/                      # Attendance tracking
├── models.py                    # AttendanceLog model
├── views.py                     # Logging views
└── urls.py                      # Attendance URLs

reports/                         # Report generation
├── views.py                     # Excel export view
└── urls.py                      # Report URLs

templates/                       # Global templates
└── home.html                    # Main dashboard

db.sqlite3                       # SQLite database
manage.py                        # Django management script
requirements.txt                 # Python dependencies
```

---

## 👤 Admin Panel

### Access
URL: http://127.0.0.1:8000/admin/

### Available Sections

1. **Users**
   - Manage usernames, passwords, permissions
   - Built-in Django users

2. **User Profiles**
   - Link users to roles (Admin/Student)
   - View enrolled fingerprints

3. **Attendance Logs**
   - View all attendance records
   - Filter by date, status, user
   - Search by username

4. **Fingerprint Scans**
   - Audit trail of all scan attempts
   - Debug sensor issues

---

## 🔧 Troubleshooting

### Sensor Connection Issues

**Problem**: "Error connecting to R307"

**Solutions**:
1. Check USB connection
2. Verify correct serial port in `r307.py`
3. Install pyserial: `pip install pyserial`
4. Check permissions (Linux/macOS):
   ```bash
   sudo chmod 666 /dev/ttyUSB0
   ```

### Fingerprint Not Recognized

**Solutions**:
1. Clean sensor surface
2. Ensure finger is properly placed
3. Re-enroll fingerprint
4. Check sensor LED indicators

### Database Errors

**Problem**: "no such table"

**Solution**:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Import Errors

**Problem**: "ModuleNotFoundError"

**Solution**:
```bash
pip install -r requirements.txt
```

### Admin Panel Not Accessible

**Problem**: 404 or permission denied

**Solution**:
```bash
# Create superuser
python manage.py createsuperuser
```

---

## 📊 Database Models

### UserProfile
- Links Django User to fingerprint template
- Stores role (Admin/Student)
- One profile per user

### FingerprintScan
- Audit trail of scan attempts
- Stores scan timestamp
- Links to user

### AttendanceLog
- Main attendance records
- Status: Present/Absent
- Auto-timestamps
- Tracks retry attempts

---

## 🔒 Security Notes

**For Production Deployment:**

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Add domain to `ALLOWED_HOSTS`
4. Use PostgreSQL/MySQL instead of SQLite
5. Enable HTTPS
6. Set up proper user permissions
7. Regular database backups

---

## 📝 Configuration

### Time Zone

Edit `settings.py`:
```python
TIME_ZONE = 'UTC'  # Change to your timezone
# Examples: 'America/New_York', 'Asia/Kolkata', 'Europe/London'
```

### Serial Port

Edit `fingerprint/r307.py`:
```python
SERIAL_PORT = '/dev/tty.usbserial-XXXXX'  # Update this
```

---

## 📞 Support

For issues or questions:
1. Check this README
2. Review console error messages
3. Verify sensor connections
4. Check Django documentation: https://docs.djangoproject.com

---

## 📄 License

[Your License Here]

---

## 👨‍💻 Development

**Author**: [Your Company Name]  
**Date**: November 2025  
**Version**: 1.0  
**Framework**: Django 5.2  
**Hardware**: R307 Fingerprint Sensor

---

**Made with ❤️ for efficient attendance management**
