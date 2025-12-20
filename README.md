# 🔐 Fingerprint Attendance System

A modern attendance management system using **Django API** + **Firebase Firestore** + **ESP32** + **R307 Fingerprint Sensor** with real-time updates.

**Backend Status:** 🟢 Running | **Frontend Status:** 🎨 Ready for Development

---

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Quick Start](#quick-start)
- [Backend Setup](#backend-setup)
- [Frontend Development](#frontend-development)
- [Firebase Configuration](#firebase-configuration)
- [ESP32 Hardware](#esp32-hardware)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🎯 System Overview

### Architecture
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   ESP32     │─────→│   Django     │─────→│  Firebase   │
│  + R307     │ HTTP │   API        │ SDK  │  Firestore  │
└─────────────┘      └──────────────┘      └─────────────┘
                            ↕                      ↕
                     ┌──────────────┐      ┌─────────────┐
                     │   Frontend   │─────→│  Real-time  │
                     │  (HTML/JS)   │ SDK  │   Updates   │
                     └──────────────┘      └─────────────┘
```

### Technology Stack
- **Backend:** Django 6.0 (API-only, no templates)
- **Database:** Firebase Firestore (cloud, real-time)
- **Hardware:** ESP32 + R307 Fingerprint Sensor
- **Frontend:** HTML/CSS/JavaScript + Firebase SDK
- **Real-time:** Firebase `onSnapshot()` listeners

---

## ⚡ Quick Start

### For Backend Developer:
```bash
# 1. Navigate to backend folder
cd backend/

# 2. Activate virtual environment (from project root)
../.venv/Scripts/Activate.ps1  # Windows
source ../.venv/bin/activate   # Linux/Mac

# 3. Start Django server
python manage.py runserver

# Server runs at: http://127.0.0.1:8000
```

### For Frontend Developer:
```bash
# Work in the frontend/ folder
cd frontend/

# All your HTML, CSS, JS files go here
# See "Frontend Development" section below
```

---

## 🔧 Backend Setup

### System Requirements
- Python 3.10+
- pip package manager
- Firebase account

### Installation

**1. Clone Repository**
```bash
git clone https://github.com/Tkapesa/Fingerprint-attendance-system-.git
cd Fingerprint-attendance-system-
```

**2. Create Virtual Environment**
```bash
python -m venv .venv

# Activate
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac
```

**3. Install Dependencies**
```bash
cd backend/
pip install -r requirements.txt
```

**Dependencies:**
- Django >= 5.2
- firebase-admin >= 6.0.0
- pandas >= 2.2.3
- openpyxl >= 3.1.5
- pyserial >= 3.5

**4. Configure Firebase**
- Get `firebase-credentials.json` from Firebase Console
- Place in `backend/` folder
- See [Firebase Configuration](#firebase-configuration) section

**5. Start Server**
```bash
cd backend/
python manage.py runserver
```

**Access:** http://127.0.0.1:8000

**Test Firebase Connection:**
```bash
cd backend/
python test_firebase_connection.py
```

### Backend API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Home page | No |
| POST | `/register/` | Student registration | No |
| POST | `/login/` | User login | No |
| GET | `/fingerprint/scan/` | Scan fingerprint | No |
| POST | `/fingerprint/enroll-own/` | Enroll own fingerprint | Yes |
| POST | `/fingerprint/enroll/` | Instructor enrolls student | Yes |
| GET | `/attendance/dashboard/` | Instructor dashboard | Yes |
| GET | `/attendance/course/<code>/` | Course attendance | Yes |

---

## 🎨 Frontend Development

### Setup

**Work in this folder:**
```
frontend/
```

All your HTML, CSS, and JavaScript files go here.

### Firebase SDK Integration

**Add to your HTML:**
```html
<!-- Firebase SDKs -->
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>

<script>
// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCJoIAWWbPXB5EHEAcXj_epzRCElh1BCgU",
  authDomain: "attendance-system-31683.firebaseapp.com",
  projectId: "attendance-system-31683",
  storageBucket: "attendance-system-31683.firebasestorage.app",
  messagingSenderId: "859845763144",
  appId: "1:859845763144:web:cfe51da2090756dbb4b87d"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
</script>
```

### Real-time Updates

**Listen for new attendance:**
```javascript
db.collection('attendance')
  .orderBy('timestamp', 'desc')
  .limit(20)
  .onSnapshot((snapshot) => {
    snapshot.docChanges().forEach((change) => {
      if (change.type === 'added') {
        const data = change.doc.data();
        console.log(`${data.student_name} marked present!`);
        // Update your UI here
      }
    });
  });
```

**Query students by course:**
```javascript
db.collection('students')
  .where('course_code', '==', 'CS101')
  .get()
  .then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
      const student = doc.data();
      console.log(student.full_name);
    });
  });
```

### Export to Excel

**Using SheetJS:**
```html
<script src="https://cdn.sheetjs.com/xlsx-latest/package/dist/xlsx.full.min.js"></script>
```

```javascript
async function exportToExcel() {
  const attendanceData = [];
  
  const snapshot = await db.collection('attendance')
    .where('course_code', '==', 'CS101')
    .get();
  
  snapshot.forEach(doc => {
    const data = doc.data();
    attendanceData.push({
      'Student Name': data.student_name,
      'Student ID': data.student_id,
      'Date': data.date,
      'Time': data.time
    });
  });
  
  const ws = XLSX.utils.json_to_sheet(attendanceData);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Attendance');
  XLSX.writeFile(wb, 'attendance_report.xlsx');
}
```

### Call Django API

**Example: Register student**
```javascript
fetch('http://127.0.0.1:8000/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'john_doe',
    email: 'john@school.com',
    password: 'secure123',
    full_name: 'John Doe',
    student_id: 'ST001',
    course: 'CS101'
  })
})
.then(response => response.json())
.then(data => console.log('Success:', data));
```

### Recommended UI Libraries
- **Bootstrap 5** - https://getbootstrap.com/
- **Tailwind CSS** - https://tailwindcss.com/
- **Chart.js** - https://www.chartjs.org/ (for graphs)
- **Font Awesome** - https://fontawesome.com/ (icons)

### Testing Your Frontend
```bash
# Option 1: Double-click HTML file
# Option 2: VS Code Live Server extension
# Option 3: Python HTTP server
cd frontend
python -m http.server 8080
```

---

## 🔥 Firebase Configuration

### Firestore Collections

#### `students/{student_id}`
```json
{
  "student_id": "ST001",
  "full_name": "John Doe",
  "email": "john@school.com",
  "course_code": "CS101",
  "fingerprint_id": 1,
  "fingerprint_enrolled": true,
  "role": "student",
  "created_at": Timestamp
}
```

#### `attendance/{attendance_id}`
```json
{
  "student_id": "ST001",
  "student_name": "John Doe",
  "course_code": "CS101",
  "date": "2025-12-20",
  "time": "09:15:30",
  "status": "present",
  "scan_method": "fingerprint",
  "timestamp": Timestamp
}
```

#### `courses/{course_code}`
```json
{
  "course_code": "CS101",
  "course_name": "Introduction to Programming",
  "instructor_name": "Prof. Smith",
  "created_at": Timestamp
}
```

#### `fingerprint_mapping/{fingerprint_id}`
```json
{
  "fingerprint_id": 1,
  "student_id": "ST001",
  "enrolled_at": Timestamp
}
```

### Initialize Firebase Collections

```bash
python initialize_firebase.py
```

This creates:
- `courses/` collection with sample courses
- `system/` collection with configuration
- Required indexes

### Firebase Console
https://console.firebase.google.com/project/attendance-system-31683

---

## 🤖 ESP32 Hardware

### Components
- ESP32 DevKit
- R307 Fingerprint Sensor
- Wires

### Wiring
```
ESP32          R307 Sensor
─────          ────────────
GPIO 16    →   TX (Yellow)
GPIO 17    →   RX (White)
3.3V       →   VCC (Red)
GND        →   GND (Black)
```

### Arduino Setup

**1. Install Libraries:**
- WiFi (built-in)
- HTTPClient (built-in)
- Adafruit Fingerprint Sensor
- ArduinoJson

**2. Configure WiFi:**
Edit `esp32_attendance_system.ino`:
```cpp
#define WIFI_SSID     "YourWiFiName"
#define WIFI_PASSWORD "YourPassword"
#define BACKEND_BASE_URL "http://10.73.3.136:8000"
```

**3. Upload Sketch:**
- Open `esp32_attendance_system.ino` in Arduino IDE
- Select board: ESP32 Dev Module
- Select correct COM port
- Click Upload

**4. Monitor Serial:**
- Open Serial Monitor (9600 baud)
- Check connection status
- View attendance logs

### ESP32 Workflow

**Enrollment:**
1. Backend triggers enrollment mode
2. ESP32 captures fingerprint (2 scans)
3. Stores template in R307 memory
4. Sends fingerprint_id to backend
5. Backend maps ID to student in Firebase

**Attendance:**
1. Student places finger on R307
2. ESP32 scans and matches fingerprint
3. Sends fingerprint_id to Django API
4. Django queries Firebase for student
5. Creates attendance record in Firebase
6. Frontend displays update in real-time

---

## 📁 Project Structure

```
Fingerprint-attendance-system/
│
├── � backend/                      # Backend Django API
│   ├── fingerprint_attendance/      # Main Django project
│   │   ├── settings.py              # Config + Firebase settings
│   │   ├── urls.py                  # Main routing
│   │   └── views.py                 # Home view
│   │
│   ├── users/                       # User management API
│   │   ├── models.py                # (Empty - using Firebase)
│   │   ├── views.py                 # Login, register
│   │   └── urls.py
│   │
│   ├── fingerprint/                 # Fingerprint operations
│   │   ├── models.py                # (Empty - using Firebase)
│   │   ├── views.py                 # Enroll, scan APIs
│   │   ├── urls.py
│   │   └── r307.py                  # R307 sensor driver
│   │
│   ├── attendance/                  # Attendance management
│   │   ├── models.py                # (Empty - using Firebase)
│   │   ├── views.py                 # Dashboard, reports
│   │   └── urls.py
│   │
│   ├── manage.py                    # Django management
│   ├── requirements.txt             # Python dependencies
│   ├── firebase-credentials.json    # Service account key
│   ├── initialize_firebase.py       # Setup Firestore
│   ├── add_student_firebase.py      # Add students
│   └── test_firebase_connection.py  # Test connection
│
├── 📁 frontend/                     # Frontend development
│   ├── realtime_dashboard.html      # Real-time attendance
│   └── (Add your HTML/CSS/JS here)
│
├── 📁 esp32_fingerprint/            # Hardware code
│   └── esp32_attendance_system.ino  # Arduino sketch
│
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── FIREBASE_SETUP_GUIDE.txt
│   ├── ESP32_QUICK_GUIDE.txt
│   └── TESTING_GUIDE.md
│
└── .venv/                           # Virtual environment
```

---

## 🔧 Troubleshooting

### Backend Issues

**Port Already in Use:**
```bash
# Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill
```

**Firebase Connection Error:**
```bash
# Test connection
cd backend/
python test_firebase_connection.py

# Check credentials file exists
ls firebase-credentials.json
```

**Module Not Found:**
```bash
cd backend/
pip install -r requirements.txt
```

### Frontend Issues

**CORS Error:**
Add to Django `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

**Firebase Permission Denied:**
- Check Firebase Console → Firestore → Rules
- Set rules to allow read/write (development only)

### ESP32 Issues

**WiFi Not Connecting:**
- Check SSID and password
- Ensure 2.4GHz network (ESP32 doesn't support 5GHz)
- Check serial monitor for error messages

**Sensor Not Detected:**
- Check wiring (TX/RX correct)
- Verify 3.3V power (not 5V)
- Test sensor with separate Arduino sketch

**Can't Upload Code:**
- Hold BOOT button while uploading
- Select correct COM port
- Install CH340 drivers (if needed)

---

## 📊 Database Schema (Firebase)

### students/ Collection
- **Document ID:** student_id (e.g., "ST001")
- **Fields:** full_name, email, course_code, fingerprint_id, fingerprint_enrolled, role, created_at, updated_at

### attendance/ Collection
- **Document ID:** Auto-generated
- **Fields:** attendance_id, student_id, student_name, course_code, date, time, status, scan_method, timestamp, fingerprint_id

### courses/ Collection
- **Document ID:** course_code (e.g., "CS101")
- **Fields:** course_name, instructor_id, instructor_name, description, created_at

### fingerprint_mapping/ Collection
- **Document ID:** fingerprint_id (e.g., "1")
- **Fields:** student_id, enrolled_at, sensor_template_data (optional)

---

## 🔒 Security Notes

### Development
- ✅ Firebase API key in frontend is safe (public by design)
- ✅ Firebase rules control data access
- ✅ Django API requires authentication for sensitive endpoints

### Production Checklist
- [ ] Set Django `DEBUG = False`
- [ ] Change `SECRET_KEY` in settings.py
- [ ] Configure Firebase security rules
- [ ] Enable HTTPS
- [ ] Set up proper authentication
- [ ] Regular database backups
- [ ] Monitor Firebase usage/costs
- [ ] Implement rate limiting
- [ ] Use environment variables for secrets

---

## 📞 Support & Resources

### Documentation
- **Django:** https://docs.djangoproject.com/
- **Firebase:** https://firebase.google.com/docs/firestore
- **ESP32:** https://docs.espressif.com/
- **R307 Sensor:** Check `ESP32_QUICK_GUIDE.txt`

### Testing
```bash
# Test backend
python manage.py runserver

# Test Firebase
python test_firebase_connection.py

# Test ESP32
# Open Serial Monitor in Arduino IDE
```

### GitHub Repository
https://github.com/Tkapesa/Fingerprint-attendance-system-.git

---

## 📝 License

[Your License Here]

---

## 🎯 Quick Reference

### Start Backend
```bash
cd backend/
.venv\Scripts\Activate.ps1  # Windows (from project root)
python manage.py runserver
```

### Start Frontend Development
```bash
cd frontend/
# Open HTML in browser or use Live Server
```

### ESP32 Upload
1. Open Arduino IDE
2. Load `esp32_fingerprint/esp32_attendance_system.ino`
3. Configure WiFi credentials
4. Upload to ESP32

### Common Commands
```bash
# Initialize Firebase
cd backend/
python initialize_firebase.py

# Add student to Firebase
cd backend/
python add_student_firebase.py

# Test Firebase connection
cd backend/
python test_firebase_connection.py
```

---

**Last Updated:** December 20, 2025  
**Backend Status:** 🟢 Running  
**Frontend Status:** 🎨 Ready for Development  
**Firebase Status:** 🟢 Connected

---

## 👨‍💻 Development

**Author**: [Your Company Name]  
**Date**: November 2025  
**Version**: 1.0  
**Framework**: Django 5.2  
**Hardware**: R307 Fingerprint Sensor

---

**Made with ❤️ for efficient attendance management**
