"""
============================================================
REPORTS VIEWS
============================================================
Generate and export attendance reports in Excel format.

Features:
- Export all attendance data to Excel
- Includes user, timestamp, status, retry count
- Uses pandas and openpyxl for Excel generation
============================================================
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from attendance.models import AttendanceLog
import pandas as pd
from datetime import datetime


@login_required
def generate_report(request):
    """
    Generate Excel report of all attendance records.
    
    Access: Authenticated users (consider restricting to admin only)
    URL: /reports/generate/
    
    Process:
        1. Fetch all attendance logs from database
        2. Convert to pandas DataFrame
        3. Export as Excel file (.xlsx)
        4. Download automatically starts
    
    Returns:
        Excel file with attendance data
    """
    # Fetch all attendance logs with user information
    logs = AttendanceLog.objects.select_related('user').all()
    
    # Convert to list of dictionaries for pandas
    data = [
        {
            'Username': log.user.username,
            'Full Name': f"{log.user.first_name} {log.user.last_name}",
            'Email': log.user.email,
            'Timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Status': log.status.capitalize(),
            'Retry Count': log.retry_count,
        }
        for log in logs
    ]
    
    # Create pandas DataFrame
    df = pd.DataFrame(data)
    
    # If no data, create empty DataFrame with headers
    if df.empty:
        df = pd.DataFrame(columns=[
            'Username', 'Full Name', 'Email', 'Timestamp', 'Status', 'Retry Count'
        ])
    
    # Generate filename with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'attendance_report_{current_date}.xlsx'
    
    # Create HTTP response with Excel content type
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    # Write DataFrame to Excel and send as response
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response

