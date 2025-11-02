"""
============================================================
FINGERPRINT ADMIN CONFIGURATION
============================================================
Register FingerprintScan model in Django admin panel.
============================================================
"""
from django.contrib import admin
from .models import FingerprintScan

# Register FingerprintScan for admin panel access
# View all scan attempts and their timestamps
admin.site.register(FingerprintScan)

