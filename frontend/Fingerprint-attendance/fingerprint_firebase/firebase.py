"""
Firebase Configuration
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
from django.conf import settings

# Initialize Firebase
try:
    cred = credentials.Certificate(settings.FIREBASE_CONFIG_PATH)
    firebase_admin.initialize_app(cred)
    
    # Get Firestore database
    db = firestore.client()
    
    print("✅ Firebase initialized successfully")
    
except Exception as e:
    print(f"❌ Firebase initialization error: {e}")
    db = None


# Firebase helper functions
class FirebaseManager:
    """Manage Firebase operations"""
    
    @staticmethod
    def create_user(email, password, user_data):
        """Create user in Firebase Authentication"""
        try:
            # Create user in Firebase Auth
            user = auth.create_user(
                email=email,
                password=password,
                display_name=user_data.get('name', '')
            )
            
            # Store additional data in Firestore
            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                **user_data,
                'uid': user.uid,
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            return user.uid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def verify_token(id_token):
        """Verify Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Token verification error: {e}")
            return None
    
    @staticmethod
    def get_user_data(uid):
        """Get user data from Firestore"""
        try:
            user_ref = db.collection('users').document(uid)
            user_data = user_ref.get()
            
            if user_data.exists:
                return user_data.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    @staticmethod
    def update_user(uid, data):
        """Update user data in Firestore"""
        try:
            user_ref = db.collection('users').document(uid)
            user_ref.update(data)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    @staticmethod
    def create_session(session_data):
        """Create a new session"""
        try:
            session_ref = db.collection('sessions').document()
            session_ref.set({
                **session_data,
                'id': session_ref.id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'is_active': True
            })
            return session_ref.id
        except Exception as e:
            print(f"Error creating session: {e}")
            return None
    
    @staticmethod
    def mark_attendance(attendance_data):
        """Mark attendance"""
        try:
            attendance_ref = db.collection('attendance').document()
            attendance_ref.set({
                **attendance_data,
                'id': attendance_ref.id,
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            return attendance_ref.id
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return None
    
    @staticmethod
    def get_active_sessions():
        """Get all active sessions"""
        try:
            sessions = db.collection('sessions')\
                        .where('is_active', '==', True)\
                        .stream()
            return [session.to_dict() for session in sessions]
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
    
    @staticmethod
    def get_courses():
        """Get all courses"""
        try:
            courses = db.collection('courses').stream()
            return [course.to_dict() for course in courses]
        except Exception as e:
            print(f"Error getting courses: {e}")
            return []
    
    @staticmethod
    def enroll_fingerprint(student_id, fingerprint_data):
        """Enroll fingerprint for student"""
        try:
            # Find student
            students = db.collection('users')\
                        .where('student_id', '==', student_id)\
                        .where('role', '==', 'student')\
                        .limit(1)\
                        .stream()
            
            student_list = list(students)
            if not student_list:
                return False
            
            student_doc = student_list[0]
            student_ref = db.collection('users').document(student_doc.id)
            
            # Update with fingerprint data
            student_ref.update({
                'fingerprint_data': fingerprint_data,
                'fingerprint_enrolled': True,
                'fingerprint_enrolled_at': firestore.SERVER_TIMESTAMP
            })
            
            # Send to ESP for enrollment
            # This would be an API call to your ESP device
            # For now, we'll just simulate it
            print(f"📤 Sending fingerprint enrollment request for student {student_id} to ESP")
            
            return True
        except Exception as e:
            print(f"Error enrolling fingerprint: {e}")
            return False