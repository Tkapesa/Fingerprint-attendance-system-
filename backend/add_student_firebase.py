"""
============================================================
ADD STUDENT TO FIREBASE DATABASE
============================================================
Simple script to add students to Firebase Realtime Database.

Usage:
    python add_student_firebase.py
============================================================
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
import sys

# Setup Django settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fingerprint_attendance.settings')

from fingerprint_attendance import settings

def add_student():
    """Add a student to Firebase database."""
    
    print("\n" + "=" * 60)
    print("ADD STUDENT TO FIREBASE")
    print("=" * 60 + "\n")
    
    # Check credentials
    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        print("❌ Firebase credentials not found!")
        print(f"   Place firebase-credentials.json in: {settings.FIREBASE_CREDENTIALS_PATH}")
        return
    
    # Initialize Firebase (if not already)
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
    
    # Get Firestore client
    db_client = firestore.client()
    
    # Get student details
    print("Enter student details:")
    print("-" * 60)
    
    student_id = input("Student ID (e.g., ST001): ").strip().upper()
    if not student_id:
        print("❌ Student ID is required!")
        return
    
    # Check if student already exists
    student_ref = db_client.collection('students').document(student_id)
    if student_ref.get().exists:
        print(f"\n⚠️  Student {student_id} already exists!")
        overwrite = input("Overwrite? (yes/no): ").strip().lower()
        if overwrite != 'yes':
            print("Cancelled.")
            return
    
    full_name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    
    # Get available courses
    courses_ref = db_client.collection('courses')
    courses = courses_ref.stream()
    
    print("\nAvailable Courses:")
    for course_doc in courses:
        course = course_doc.to_dict()
        print(f"  - {course_doc.id}: {course.get('course_name', 'N/A')}")
    
    course_code = input("\nCourse Code (e.g., CS101): ").strip().upper()
    
    fingerprint_id = input("Fingerprint ID (leave empty if not enrolled yet): ").strip()
    fingerprint_id = int(fingerprint_id) if fingerprint_id else None
    
    # Create student data
    student_data = {
        'student_id': student_id,
        'full_name': full_name,
        'email': email,
        'course_code': course_code,
        'fingerprint_enrolled': fingerprint_id is not None,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    if fingerprint_id:
        student_data['fingerprint_id'] = fingerprint_id
    
    # Save to Firestore
    print("\nSaving to Firestore...")
    try:
        student_ref.set(student_data)
        print(f"✅ Student {student_id} added successfully!")
        
        # If fingerprint ID provided, create mapping
        if fingerprint_id:
            mapping_ref = db_client.collection('fingerprint_mapping').document(str(fingerprint_id))
            mapping_ref.set({'student_id': student_id})
            print(f"✅ Fingerprint mapping created: {fingerprint_id} → {student_id}")
        
        # Display summary
        print("\n" + "-" * 60)
        print("STUDENT ADDED:")
        print(f"  Student ID: {student_id}")
        print(f"  Name: {full_name}")
        print(f"  Email: {email}")
        print(f"  Course: {course_code}")
        print(f"  Fingerprint: {'ID ' + str(fingerprint_id) if fingerprint_id else 'Not enrolled'}")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def add_multiple_students():
    """Add multiple students in batch."""
    
    print("\n" + "=" * 60)
    print("BATCH ADD STUDENTS TO FIREBASE")
    print("=" * 60 + "\n")
    
    # Check credentials
    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        print("❌ Firebase credentials not found!")
        return
    
    # Initialize Firebase
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
    
    db_client = firestore.client()
    
    students = []
    
    print("Enter students (press Enter with empty Student ID to finish):")
    print("-" * 60)
    
    while True:
        print()
        student_id = input("Student ID (or Enter to finish): ").strip().upper()
        if not student_id:
            break
        
        full_name = input("  Full Name: ").strip()
        email = input("  Email: ").strip()
        course_code = input("  Course Code: ").strip().upper()
        fingerprint_id = input("  Fingerprint ID (optional): ").strip()
        
        students.append({
            'student_id': student_id,
            'full_name': full_name,
            'email': email,
            'course_code': course_code,
            'fingerprint_id': int(fingerprint_id) if fingerprint_id else None,
            'fingerprint_enrolled': bool(fingerprint_id),
            'created_at': firestore.SERVER_TIMESTAMP
        })
    
    if not students:
        print("\nNo students to add.")
        return
    
    # Confirm
    print(f"\n{len(students)} student(s) to add:")
    for s in students:
        print(f"  - {s['student_id']}: {s['full_name']}")
    
    confirm = input("\nProceed? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return
    
    # Add to Firestore
    print("\nAdding students...")
    success_count = 0
    
    for student in students:
        try:
            student_id = student['student_id']
            fingerprint_id = student.pop('fingerprint_id', None)
            
            # Add student
            student_ref = db_client.collection('students').document(student_id)
            student_ref.set(student)
            
            # Add fingerprint mapping if provided
            if fingerprint_id:
                mapping_ref = db_client.collection('fingerprint_mapping').document(str(fingerprint_id))
                mapping_ref.set({'student_id': student_id})
            
            print(f"  ✅ {student_id}: {student['full_name']}")
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ {student_id}: {str(e)}")
    
    print(f"\n✅ {success_count}/{len(students)} students added successfully!")

def main():
    """Main menu."""
    
    while True:
        print("\n" + "=" * 60)
        print("FIREBASE STUDENT MANAGEMENT")
        print("=" * 60)
        print("\n1. Add Single Student")
        print("2. Add Multiple Students (Batch)")
        print("3. Exit")
        print()
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            add_student()
            input("\nPress Enter to continue...")
        elif choice == '2':
            add_multiple_students()
            input("\nPress Enter to continue...")
        elif choice == '3':
            print("\nGoodbye!")
            break
        else:
            print("\n❌ Invalid option!")

if __name__ == "__main__":
    main()
