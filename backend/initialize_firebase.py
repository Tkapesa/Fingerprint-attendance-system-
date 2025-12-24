"""
============================================================
FIREBASE FIRESTORE INITIALIZATION SCRIPT
============================================================
This script initializes the Firebase Firestore Database with
the required structure for the attendance system.

Run this ONCE after setting up Firebase credentials.

Usage:
    python initialize_firebase.py
============================================================
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Import settings to get Firebase configuration
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fingerprint_attendance.settings')

from fingerprint_attendance import settings

def initialize_firebase():
    """Initialize Firebase Firestore connection and create database structure."""
    
    print("=" * 60)
    print("FIREBASE FIRESTORE INITIALIZATION")
    print("=" * 60)
    print()
    
    # Check if credentials file exists
    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        print("❌ ERROR: Firebase credentials file not found!")
        print(f"   Expected location: {settings.FIREBASE_CREDENTIALS_PATH}")
        print()
        print("   Steps to fix:")
        print("   1. Go to Firebase Console")
        print("   2. Project Settings > Service Accounts")
        print("   3. Generate New Private Key")
        print("   4. Save as 'firebase-credentials.json' in project root")
        return False
    
    try:
        # Initialize Firebase Admin SDK
        print("1. Connecting to Firebase Firestore...")
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        
        # Check if already initialized
        try:
            firebase_admin.get_app()
            print("   ⚠️  Already initialized, using existing connection")
        except ValueError:
            firebase_admin.initialize_app(cred)
        
        print("   ✅ Connected to Firebase Firestore!")
        print(f"   Project ID: {settings.FIREBASE_PROJECT_ID}")
        print()
        
        # Get Firestore client
        db_client = firestore.client()
        
        # Create initial collections and documents
        print("2. Creating Firestore collections...")
        
        # Create sample courses
        print("   Creating 'courses' collection...")
        courses_data = [
            {
                'course_code': 'CS101',
                'course_name': 'Introduction to Programming',
                'instructor': 'Prof. Smith',
                'description': 'Basic programming concepts with Python',
                'created_at': firestore.SERVER_TIMESTAMP
            },
            {
                'course_code': 'CS201',
                'course_name': 'Data Structures',
                'instructor': 'Prof. Johnson',
                'description': 'Advanced data structures and algorithms',
                'created_at': firestore.SERVER_TIMESTAMP
            },
            {
                'course_code': 'MATH101',
                'course_name': 'Calculus I',
                'instructor': 'Prof. Williams',
                'description': 'Introduction to calculus',
                'created_at': firestore.SERVER_TIMESTAMP
            }
        ]
        
        for course in courses_data:
            db_client.collection('courses').document(course['course_code']).set(course)
        
        print("   ✅ 'courses' collection created with sample data")
        
        # Create system_info document
        print("   Creating 'system_info' document...")
        db_client.collection('system').document('info').set({
            'initialized_at': firestore.SERVER_TIMESTAMP,
            'version': '1.0',
            'database_type': 'Firestore',
            'last_updated': firestore.SERVER_TIMESTAMP
        })
        print("   ✅ 'system_info' created")
        
        print()
        print("=" * 60)
        print("✅ FIREBASE FIRESTORE INITIALIZED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Add students using: python add_student_firebase.py")
        print("2. Configure ESP32 with Firebase credentials")
        print("3. Enroll fingerprints and map to student IDs")
        print("4. Use onSnapshot in frontend for real-time updates")
        print()
        print("Firestore Collections Created:")
        print("  - courses/")
        print("  - students/ (will be created when adding students)")
        print("  - attendance/ (will be created when marking attendance)")
        print("  - fingerprint_mapping/ (will be created when mapping)")
        print()
        print("Sample student document structure:")
        print("""
        students/ST001 {
          "full_name": "John Doe",
          "email": "john@school.com",
          "student_id": "ST001",
          "course_code": "CS101",
          "fingerprint_id": 1,
          "fingerprint_enrolled": true,
          "created_at": Timestamp
        }
        """)
        
        return True
        
    except Exception as e:
        print()
        print("❌ ERROR:", str(e))
        print()
        print("Common issues:")
        print("1. Invalid credentials file")
        print("2. Wrong database URL in settings.py")
        print("3. No internet connection")
        print("4. Firebase project doesn't exist")
        return False

def test_connection():
    """Test Firestore read/write operations."""
    print()
    print("Testing Firestore operations...")
    print()
    
    try:
        db_client = firestore.client()
        
        # Test write
        print("1. Testing write operation...")
        test_ref = db_client.collection('_test').document('connection_test')
        test_ref.set({
            'timestamp': firestore.SERVER_TIMESTAMP,
            'message': 'Connection test successful'
        })
        print("   ✅ Write successful")
        
        # Test read
        print("2. Testing read operation...")
        doc = test_ref.get()
        if doc.exists:
            print("   ✅ Read successful")
            print(f"   Data: {doc.to_dict()['message']}")
        
        # Clean up test data
        print("3. Cleaning up test data...")
        test_ref.delete()
        print("   ✅ Delete successful")
        
        print()
        print("✅ All tests passed!")
        print("✅ Firestore is ready for real-time onSnapshot listeners!")
        return True
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Initialize database
    success = initialize_firebase()
    
    if success:
        # Test connection
        test_connection()
    else:
        print()
        print("Please fix the errors above and try again.")
        sys.exit(1)
