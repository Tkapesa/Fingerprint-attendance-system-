"""
ESP32 Fingerprint Scanner Communication
"""
import requests
import time
from django.conf import settings

class ESPCommunicator:
    """Communicate with ESP32 fingerprint scanner"""
    
    def __init__(self):
        self.base_url = settings.ESP_API_URL
        self.api_key = settings.ESP_API_KEY
    
    def enroll_fingerprint(self, student_id, student_name):
        """Send enrollment request to ESP"""
        try:
            response = requests.post(
                f"{self.base_url}/enroll",
                json={
                    'student_id': student_id,
                    'student_name': student_name,
                    'action': 'enroll',
                    'timestamp': int(time.time())
                },
                headers={'X-API-Key': self.api_key},
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Enrollment request sent successfully',
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'ESP Error: {response.status_code}',
                    'error': response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': 'ESP device timeout - check connection'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def verify_fingerprint(self):
        """Request fingerprint verification"""
        try:
            response = requests.post(
                f"{self.base_url}/verify",
                json={'action': 'verify'},
                headers={'X-API-Key': self.api_key},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return {
                        'success': True,
                        'student_id': data.get('student_id'),
                        'confidence': data.get('confidence')
                    }
                else:
                    return {
                        'success': False,
                        'message': data.get('message', 'Verification failed')
                    }
                    
        except requests.exceptions.RequestException:
            return {
                'success': False,
                'message': 'Cannot connect to ESP device'
            }
    
    def get_status(self):
        """Get ESP device status"""
        try:
            response = requests.get(
                f"{self.base_url}/status",
                headers={'X-API-Key': self.api_key},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'status': 'offline', 'error': response.text}
                
        except requests.exceptions.RequestException:
            return {'status': 'offline', 'error': 'Connection failed'}
    
    def delete_fingerprint(self, student_id):
        """Delete fingerprint from ESP"""
        try:
            response = requests.post(
                f"{self.base_url}/delete",
                json={'student_id': student_id, 'action': 'delete'},
                headers={'X-API-Key': self.api_key}
            )
            
            return response.status_code == 200
            
        except requests.exceptions.RequestException:
            return False