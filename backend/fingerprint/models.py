"""
============================================================
FINGERPRINT SCAN MODEL
============================================================
Stores individual fingerprint scan records for tracking and debugging.
Note: This is separate from UserProfile.fingerprint_template
============================================================
"""
from django.db import models
from django.contrib.auth.models import User

class FingerprintScan(models.Model):
    """
    Record of each fingerprint scan attempt.
    
    Fields:
        user: Which user performed the scan
        scan_data: Raw fingerprint data from the sensor
        scan_time: When the scan was performed (auto-set)
    
    Purpose: Audit trail and debugging - track all scan attempts
    """
    
    # User who performed the scan
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Raw scan data from fingerprint sensor
    scan_data = models.BinaryField()
    
    # Timestamp - automatically set when record is created
    scan_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of scan record"""
        return f"Scan for {self.user.username} at {self.scan_time}"

