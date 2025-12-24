import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

# Setup Django environment
sys.path.append(r'C:\Users\EJAY MASALU\OneDrive\Desktop\Simaclaverly\Attendance Main\Fingerprint-attendance-system-\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fingerprint_attendance.settings')

from fingerprint_attendance import settings

# Initialize Firebase
cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Add a test user
user_data = {
    'email': 'test@example.com',
    'role': 'teacher',
    'created_at': firestore.SERVER_TIMESTAMP
}

db.collection('users').document('test_user_id').set(user_data)
print('Test user added successfully!')

# Also add an admin user
admin_data = {
    'email': 'admin@example.com',
    'role': 'admin',
    'created_at': firestore.SERVER_TIMESTAMP
}

db.collection('users').document('admin_user_id').set(admin_data)
print('Test admin added successfully!')