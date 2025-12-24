import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fingerprint_firebase.settings')
try:
    django.setup()
    print("✅ Django setup successful")
    
    # Test imports
    from apps.auth import views
    print("✅ Auth views imported")
    
    from django.core.management import execute_from_command_line
    print("✅ Django management commands available")
    
except Exception as e:
    print(f"❌ Error: {e}")