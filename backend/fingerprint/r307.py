"""
============================================================
R307 FINGERPRINT SENSOR INTERFACE
============================================================
Handles communication with R307 fingerprint sensor module.

Hardware: R307 Optical Fingerprint Scanner
Connection: Serial USB (UART)
Baud Rate: 57600

IMPORTANT SETUP INSTRUCTIONS:
1. Connect R307 sensor to computer via USB-to-Serial adapter
2. Find your serial port:
   - macOS: Run "ls /dev/tty.*" in terminal
   - Linux: Run "ls /dev/ttyUSB*" or "ls /dev/ttyACM*"
   - Windows: Check Device Manager for COM port (e.g., COM3)
3. Update SERIAL_PORT below with your actual port
4. Install required package: pip install pyserial
============================================================
"""
import serial
import time

# ========== CONFIGURATION ==========
# TODO: Update this with your actual serial port!
SERIAL_PORT = '/dev/tty.usbserial-XXXXX'  # macOS/Linux example
# SERIAL_PORT = 'COM3'  # Windows example
BAUD_RATE = 57600  # R307 default baud rate

class R307:
    """
    R307 Fingerprint Sensor Interface Class
    
    Methods:
        __init__: Initialize serial connection to sensor
        close: Close serial connection
        enroll_fingerprint: Capture and store fingerprint template
        scan_fingerprint: Scan finger and return template data
        match_fingerprint: Compare two fingerprint templates
    """
    
    def __init__(self, port=SERIAL_PORT, baudrate=BAUD_RATE):
        """
        Initialize connection to R307 sensor.
        
        Args:
            port: Serial port path (e.g., '/dev/ttyUSB0' or 'COM3')
            baudrate: Communication speed (default: 57600)
        """
        try:
            # Attempt to open serial connection
            self.ser = serial.Serial(port, baudrate, timeout=2)
            print(f"✓ Connected to R307 sensor on {port}")
        except Exception as e:
            # Connection failed - sensor not connected or wrong port
            print(f"✗ Error connecting to R307: {e}")
            print("  Check: 1) Sensor is connected, 2) Correct port in settings")
            self.ser = None

    def close(self):
        """Close the serial connection to the sensor."""
        if self.ser:
            self.ser.close()
            print("✓ R307 connection closed")

    def enroll_fingerprint(self):
        """
        Enroll a new fingerprint.
        
        Process:
        1. User places finger on sensor
        2. Sensor captures image
        3. Converts to template
        4. Returns template data for storage
        
        Returns:
            bytes: Fingerprint template data, or None if failed
        """
        if not self.ser:
            print("✗ Sensor not connected")
            return None
        
        print("👆 Place finger on sensor for enrollment...")
        time.sleep(2)  # Wait for finger placement
        
        # TODO: Implement actual R307 enrollment protocol
        # This is a placeholder - replace with real sensor commands
        print("✓ Fingerprint enrolled (simulated)")
        return b"FAKE_TEMPLATE_DATA"  # Replace with actual template

    def scan_fingerprint(self):
        """
        Scan fingerprint for matching.
        
        Process:
        1. User places finger on sensor
        2. Sensor captures image
        3. Converts to template for comparison
        
        Returns:
            bytes: Scanned fingerprint template, or None if failed
        """
        if not self.ser:
            print("✗ Sensor not connected")
            return None
        
        print("👆 Place finger on sensor for scanning...")
        time.sleep(2)  # Wait for finger placement
        
        # TODO: Implement actual R307 scan protocol
        # This is a placeholder - replace with real sensor commands
        print("✓ Fingerprint scanned (simulated)")
        return b"FAKE_SCAN_DATA"  # Replace with actual scan

    def match_fingerprint(self, template, scan):
        """
        Compare two fingerprint templates.
        
        Args:
            template: Stored fingerprint template (from enrollment)
            scan: New scan to compare against template
            
        Returns:
            bool: True if fingerprints match, False otherwise
        """
        if not self.ser:
            return False
        
        # TODO: Implement actual R307 matching algorithm
        # Simple comparison for now - replace with sensor's match function
        return template == scan
 