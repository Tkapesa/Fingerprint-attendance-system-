/*
  ESP32 Attendance System - Full Implementation
  Author: simaclaverly
  Purpose: Fingerprint-based attendance with Firebase Firestore
  Hardware: ESP32 + R307 Fingerprint Sensor
  
  WIRING:
  R307 VCC (Red)   → ESP32 3.3V
  R307 GND (Black) → ESP32 GND
  R307 TX (White)  → ESP32 GPIO16 (RX2)
  R307 RX (Green)  → ESP32 GPIO17 (TX2)
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Fingerprint.h>
#include <ArduinoJson.h>
#include <time.h>

// ============ CONFIGURATION - CHANGE THESE ============
const char* WIFI_SSID = "YOUR_WIFI_NAME";           // Change to your WiFi name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";   // Change to your WiFi password

// Firebase Configuration (Already set for your project)
#define FIREBASE_PROJECT_ID "attendance-system-31683"
#define FIREBASE_API_KEY "AIzaSyCJoIAWWbPXB5EHEAcXj_epzRCElh1BCgU"

// Firestore REST API URL
const String FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/" + 
                             String(FIREBASE_PROJECT_ID) + "/databases/(default)/documents/";

// ============ HARDWARE PINS ============
#define SENSOR_RX 16  // ESP32 RX2 → R307 TX
#define SENSOR_TX 17  // ESP32 TX2 → R307 RX

// ============ GLOBAL OBJECTS ============
HardwareSerial sensorSerial(2);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&sensorSerial);

// ============ GLOBAL VARIABLES ============
unsigned long lastScanTime = 0;
const unsigned long SCAN_DELAY = 3000;  // 3 seconds between scans

// Time configuration
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;     // Change to your timezone offset (e.g., 3600 for +1 hour)
const int daylightOffset_sec = 0;

// ============================================================
// SETUP - Runs once when ESP32 starts
// ============================================================
void setup() {
  // Start Serial communication
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n\n=================================");
  Serial.println("ESP32 Attendance System Started");
  Serial.println("=================================\n");

  // Step 1: Initialize fingerprint sensor
  Serial.println("Step 1: Initializing R307 Sensor...");
  sensorSerial.begin(57600, SERIAL_8N1, SENSOR_RX, SENSOR_TX);
  
  if (finger.verifyPassword()) {
    Serial.println("✅ R307 Sensor Connected!");
    Serial.print("   Enrolled fingerprints: ");
    Serial.println(finger.templateCount);
  } else {
    Serial.println("❌ R307 Sensor NOT FOUND!");
    Serial.println("   Check wiring and restart");
    while (1) { delay(1000); }  // Stop here
  }

  // Step 2: Connect to WiFi
  Serial.println("\nStep 2: Connecting to WiFi...");
  Serial.print("   Network: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi Connected!");
    Serial.print("   IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ WiFi Connection Failed!");
    Serial.println("   System will work offline (limited)");
  }

  // Step 3: Sync time with internet
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nStep 3: Synchronizing time...");
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
    
    struct tm timeinfo;
    if (getLocalTime(&timeinfo)) {
      Serial.println("✅ Time synchronized!");
      Serial.print("   Current: ");
      Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
    }
  }

  // System ready
  Serial.println("\n=================================");
  Serial.println("✅ SYSTEM READY!");
  Serial.println("Place finger on sensor...");
  Serial.println("=================================\n");
}

// ============================================================
// LOOP - Runs continuously
// ============================================================
void loop() {
  // Wait for cooldown period
  if (millis() - lastScanTime < SCAN_DELAY) {
    delay(50);
    return;
  }

  // Check if finger is on sensor
  uint8_t result = finger.getImage();
  
  if (result == FINGERPRINT_OK) {
    Serial.println("\n👆 Finger detected!");
    lastScanTime = millis();
    
    // Process the fingerprint
    scanFingerprint();
  }
  
  delay(50);
}

// ============================================================
// SCAN FINGERPRINT - Main fingerprint processing
// ============================================================
void scanFingerprint() {
  // Convert image to template
  Serial.println("   Converting image...");
  uint8_t result = finger.image2Tz();
  
  if (result != FINGERPRINT_OK) {
    Serial.println("   ❌ Failed to convert image");
    return;
  }
  
  // Search for match in sensor database
  Serial.println("   Searching for match...");
  result = finger.fingerSearch();
  
  if (result == FINGERPRINT_OK) {
    // Match found!
    Serial.println("   ✅ Match Found!");
    Serial.print("   Fingerprint ID: ");
    Serial.print(finger.fingerID);
    Serial.print(" (Confidence: ");
    Serial.print(finger.confidence);
    Serial.println(")");
    
    // Mark attendance in Firestore
    if (WiFi.status() == WL_CONNECTED) {
      markAttendance(finger.fingerID, finger.confidence);
    } else {
      Serial.println("   ⚠️ No WiFi - Cannot save attendance");
    }
    
  } else if (result == FINGERPRINT_NOTFOUND) {
    Serial.println("   ❌ No Match Found");
    Serial.println("   Fingerprint not enrolled");
  } else {
    Serial.println("   ❌ Search Error");
  }
  
  Serial.println("-----------------------------------\n");
}

// ============================================================
// MARK ATTENDANCE - Save to Firestore
// ============================================================
void markAttendance(int fingerprintID, int confidence) {
  Serial.println("\n📡 Connecting to Firestore...");
  
  HTTPClient http;
  
  // ===== STEP 1: Get Student ID from fingerprint mapping =====
  Serial.println("   Step 1: Looking up student...");
  String mappingURL = FIRESTORE_URL + "fingerprint_mapping/" + String(fingerprintID) + 
                      "?key=" + FIREBASE_API_KEY;
  
  http.begin(mappingURL);
  int httpCode = http.GET();
  
  String studentID = "";
  
  if (httpCode == 200) {
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, http.getString());
    
    if (doc["fields"]["student_id"]["stringValue"]) {
      studentID = doc["fields"]["student_id"]["stringValue"].as<String>();
      Serial.print("      Found: ");
      Serial.println(studentID);
    } else {
      Serial.println("      ❌ Mapping not found!");
      http.end();
      return;
    }
  } else {
    Serial.println("      ❌ Failed to get mapping!");
    Serial.print("      HTTP Code: ");
    Serial.println(httpCode);
    http.end();
    return;
  }
  http.end();
  
  // ===== STEP 2: Get Student Details =====
  Serial.println("   Step 2: Getting student info...");
  String studentURL = FIRESTORE_URL + "students/" + studentID + "?key=" + FIREBASE_API_KEY;
  
  http.begin(studentURL);
  httpCode = http.GET();
  
  String studentName = "";
  String courseCode = "";
  
  if (httpCode == 200) {
    DynamicJsonDocument doc(2048);
    deserializeJson(doc, http.getString());
    
    studentName = doc["fields"]["full_name"]["stringValue"].as<String>();
    courseCode = doc["fields"]["course_code"]["stringValue"].as<String>();
    
    Serial.print("      Name: ");
    Serial.println(studentName);
    Serial.print("      Course: ");
    Serial.println(courseCode);
  } else {
    Serial.println("      ❌ Student not found!");
    http.end();
    return;
  }
  http.end();
  
  // ===== STEP 3: Check if already marked today =====
  String today = getDate();
  String attendanceID = studentID + "_" + today + "_" + courseCode;
  
  Serial.println("   Step 3: Checking today's attendance...");
  String checkURL = FIRESTORE_URL + "attendance/" + attendanceID + "?key=" + FIREBASE_API_KEY;
  
  http.begin(checkURL);
  httpCode = http.GET();
  
  if (httpCode == 200) {
    Serial.println("      ⚠️ Already marked today!");
    
    DynamicJsonDocument doc(2048);
    deserializeJson(doc, http.getString());
    String timeMarked = doc["fields"]["time"]["stringValue"].as<String>();
    
    // Show welcome message
    Serial.println("\n╔════════════════════════════════════╗");
    Serial.print("║ Welcome back, ");
    Serial.print(studentName);
    for(int i=studentName.length(); i<20; i++) Serial.print(" ");
    Serial.println("║");
    Serial.print("║ Already present (");
    Serial.print(timeMarked);
    Serial.println(")        ║");
    Serial.println("╚════════════════════════════════════╝\n");
    
    http.end();
    return;
  }
  http.end();
  
  // ===== STEP 4: Create Attendance Record =====
  Serial.println("   Step 4: Marking attendance...");
  
  String timestamp = getTimestamp();
  String timeOnly = getTime();
  
  // Build Firestore document
  DynamicJsonDocument attendanceDoc(2048);
  attendanceDoc["fields"]["student_id"]["stringValue"] = studentID;
  attendanceDoc["fields"]["student_name"]["stringValue"] = studentName;
  attendanceDoc["fields"]["course_code"]["stringValue"] = courseCode;
  attendanceDoc["fields"]["date"]["stringValue"] = today;
  attendanceDoc["fields"]["time"]["stringValue"] = timeOnly;
  attendanceDoc["fields"]["timestamp"]["timestampValue"] = timestamp;
  attendanceDoc["fields"]["status"]["stringValue"] = "present";
  attendanceDoc["fields"]["scan_method"]["stringValue"] = "fingerprint";
  attendanceDoc["fields"]["fingerprint_id"]["integerValue"] = fingerprintID;
  attendanceDoc["fields"]["confidence"]["integerValue"] = confidence;
  
  String jsonPayload;
  serializeJson(attendanceDoc, jsonPayload);
  
  // POST to Firestore
  String createURL = FIRESTORE_URL + "attendance?documentId=" + attendanceID + 
                     "&key=" + FIREBASE_API_KEY;
  
  http.begin(createURL);
  http.addHeader("Content-Type", "application/json");
  httpCode = http.POST(jsonPayload);
  
  if (httpCode == 200 || httpCode == 201) {
    Serial.println("      ✅ Attendance Marked!");
    
    // Success message
    Serial.println("\n╔════════════════════════════════════╗");
    Serial.print("║ ✅ Welcome, ");
    Serial.print(studentName);
    for(int i=studentName.length(); i<24; i++) Serial.print(" ");
    Serial.println("║");
    Serial.print("║ 📚 Course: ");
    Serial.print(courseCode);
    for(int i=courseCode.length(); i<24; i++) Serial.print(" ");
    Serial.println("║");
    Serial.print("║ 🕐 Time: ");
    Serial.print(timeOnly);
    for(int i=timeOnly.length(); i<26; i++) Serial.print(" ");
    Serial.println("║");
    Serial.println("║ Status: PRESENT                    ║");
    Serial.println("╚════════════════════════════════════╝\n");
    
  } else {
    Serial.println("      ❌ Failed to mark attendance!");
    Serial.print("      HTTP Code: ");
    Serial.println(httpCode);
  }
  
  http.end();
}

// ============================================================
// HELPER FUNCTIONS - Time formatting
// ============================================================

// Get current date (YYYY-MM-DD)
String getDate() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "2025-01-01";
  }
  char buffer[11];
  strftime(buffer, sizeof(buffer), "%Y-%m-%d", &timeinfo);
  return String(buffer);
}

// Get current timestamp (ISO 8601 format)
String getTimestamp() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "2025-01-01T00:00:00Z";
  }
  char buffer[25];
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
  return String(buffer);
}

// Get current time (HH:MM:SS)
String getTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "00:00:00";
  }
  char buffer[9];
  strftime(buffer, sizeof(buffer), "%H:%M:%S", &timeinfo);
  return String(buffer);
}
