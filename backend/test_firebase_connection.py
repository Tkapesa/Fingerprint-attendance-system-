"""
Test Firebase Connection Script
Checks if backend can connect to Firebase Firestore
"""

import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fingerprint_attendance.settings')

import firebase_admin
from firebase_admin import credentials, firestore
from fingerprint_attendance import settings
from datetime import datetime

def test_firebase_connection():
    """Test Firebase Firestore connection"""
    
    print("=" * 60)
    print("FIREBASE CONNECTION TEST")
    print("=" * 60)
    print()
    
    # Check if credentials file exists
    print("1. Checking credentials file...")
    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        print("   ❌ FAILED: firebase-credentials.json not found!")
        print(f"   Expected location: {settings.FIREBASE_CREDENTIALS_PATH}")
        return False
    print(f"   ✅ Found: {settings.FIREBASE_CREDENTIALS_PATH}")
    print()
    
    # Initialize Firebase
    print("2. Initializing Firebase Admin SDK...")
    try:
        # Check if already initialized
        try:
            app = firebase_admin.get_app()
            print("   ⚠️  Already initialized, using existing connection")
        except ValueError:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("   ✅ Firebase Admin SDK initialized!")
        
        print(f"   Project ID: {settings.FIREBASE_PROJECT_ID}")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False
    
    # Get Firestore client
    print("3. Connecting to Firestore database...")
    try:
        db = firestore.client()
        print("   ✅ Firestore client created!")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False
    
    # Test write operation
    print("4. Testing WRITE operation...")
    try:
        test_ref = db.collection('_connection_test').document('test')
        test_data = {
            'message': 'Backend connected successfully',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'test_date': datetime.now().isoformat()
        }
        test_ref.set(test_data)
        print("   ✅ Write successful!")
        print(f"   Wrote to: _connection_test/test")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False
    
    # Test read operation
    print("5. Testing READ operation...")
    try:
        doc = test_ref.get()
        if doc.exists:
            data = doc.to_dict()
            print("   ✅ Read successful!")
            print(f"   Data: {data['message']}")
            print()
        else:
            print("   ❌ FAILED: Document doesn't exist")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False
    
    # Check existing collections
    print("6. Checking existing collections...")
    try:
        collections = db.collections()
        collection_names = [col.id for col in collections]
        
        if collection_names:
            print(f"   ✅ Found {len(collection_names)} collection(s):")
            for name in collection_names:
                # Count documents in each collection
                docs = db.collection(name).limit(5).stream()
                doc_count = sum(1 for _ in docs)
                print(f"      - {name}/ ({doc_count}+ documents)")
        else:
            print("   ⚠️  No collections found (database is empty)")
            print("   💡 Run: python initialize_firebase.py to setup collections")
        print()
    except Exception as e:
        print(f"   ⚠️  Could not list collections: {str(e)}")
        print()
    
    # Clean up test data
    print("7. Cleaning up test data...")
    try:
        test_ref.delete()
        print("   ✅ Test document deleted")
        print()
    except Exception as e:
        print(f"   ⚠️  Could not delete test document: {str(e)}")
        print()
    
    # Summary
    print("=" * 60)
    print("✅ FIREBASE CONNECTION TEST PASSED!")
    print("=" * 60)
    print()
    print("Your Django backend IS connected to Firebase!")
    print()
    print("Firebase Configuration:")
    print(f"  • Project ID: {settings.FIREBASE_PROJECT_ID}")
    print(f"  • Database: {settings.FIRESTORE_DATABASE}")
    print(f"  • API Key: {settings.FIREBASE_API_KEY[:20]}...")
    print()
    print("Next steps:")
    print("  1. Run: python initialize_firebase.py (if not done)")
    print("  2. Start Django server: python manage.py runserver")
    print("  3. Test attendance marking")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = test_firebase_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)
