/*
============================================================
ESP32 FINGERPRINT ATTENDANCE SYSTEM WITH FIRESTORE
============================================================
Hardware: ESP32 + R307 Fingerprint Sensor
Database: Firebase Firestore
Connection: WiFi + REST API

Wiring (R307 to ESP32):
- R307 VCC (Red)    → ESP32 3.3V or 5V
- R307 GND (Black)  → ESP32 GND
- R307 TX (White)   → ESP32 RX2 (GPIO 16)
- R307 RX (Green)   → ESP32 TX2 (GPIO 17)

Arduino IDE Setup:
1. Install ESP32 board support
2. Install libraries:
   - Adafruit Fingerprint Sensor Library
   - ArduinoJson (by Benoit Blanchon)
3. Tools → Board → ESP32 Dev Module
4. Upload this code

============================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Fingerprint.h>
#include <ArduinoJson.h>
#include <time.h>

// ========== WIFI CONFIGURATION ==========
#define WIFI_SSID "YOUR_WIFI_SSID"          // Change this
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"  // Change this

// ========== FIREBASE CONFIGURATION ==========
#define FIREBASE_PROJECT_ID "attendance-system-31683"
#define FIREBASE_API_KEY "AIzaSyCJoIAWWbPXB5EHEAcXj_epzRCElh1BCgU"

// Firestore REST API endpoints
const String FIRESTORE_BASE_URL = "https://firestore.googleapis.com/v1/projects/" + 
                                   String(FIREBASE_PROJECT_ID) + "/databases/(default)/documents/";

// ========== HARDWARE CONFIGURATION ==========
#define SENSOR_RX 16  // ESP32 GPIO16 → R307 TX
#define SENSOR_TX 17  // ESP32 GPIO17 → R307 RX

// ========== GLOBAL OBJECTS ==========
HardwareSerial fingerprintSerial(2);  // Use UART2
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fingerprintSerial);

// ========== GLOBAL VARIABLES ==========
bool wifiConnected = false;
unsigned long lastScanTime = 0;
const unsigned long SCAN_COOLDOWN = 3000;  // 3 seconds between scans

// NTP Time Server
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;      // Adjust for your timezone (0 = UTC)
const int daylightOffset_sec = 0;

// ========== SETUP FUNCTION ==========
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n========================================");
  Serial.println("ESP32 FINGERPRINT ATTENDANCE SYSTEM");
  Serial.println("With Firebase Firestore");
  Serial.println("========================================\n");
  
  // 1. Initialize Fingerprint Sensor
  initializeSensor();
  
  // 2. Connect to WiFi
  connectWiFi();
  
  // 3. Initialize Time
  if (wifiConnected) {
    initializeTime();
  }
  
  // 4. System Ready
  Serial.println("\n========================================");
  if (wifiConnected) {
    Serial.println("✅ SYSTEM READY!");
    Serial.println("Place finger on sensor to mark attendance");
  } else {
    Serial.println("⚠️  WiFi not connected - system limited");
  }
  Serial.println("========================================\n");
}

// ========== MAIN LOOP ==========
void loop() {
  // Check scan cooldown
  if (millis() - lastScanTime < SCAN_COOLDOWN) {
    return;
  }
  
  // Check for finger
  uint8_t result = finger.getImage();
  
  if (result == FINGERPRINT_OK) {
    Serial.println("\n👆 Finger detected!");
    lastScanTime = millis();
    processFingerprintScan();
  }
  
  delay(50);
}

// ========== INITIALIZE FINGERPRINT SENSOR ==========
void initializeSensor() {
  Serial.println("1. Initializing R307 Sensor...");
  
  fingerprintSerial.begin(57600, SERIAL_8N1, SENSOR_RX, SENSOR_TX);
  
  if (finger.verifyPassword()) {
    Serial.println("   ✅ R307 Sensor Found!");
    Serial.print("   Templates stored: ");
    Serial.println(finger.templateCount);
  } else {
    Serial.println("   ❌ R307 Sensor NOT Found!");
    Serial.println("   Check wiring and power");
    while (1) { delay(1000); }
  }
}

// ========== CONNECT TO WIFI ==========
void connectWiFi() {
  Serial.println("\n2. Connecting to WiFi...");
  Serial.print("   SSID: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println("\n   ✅ WiFi Connected!");
    Serial.print("   IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiConnected = false;
    Serial.println("\n   ❌ WiFi Connection Failed!");
  }
}

// ========== INITIALIZE TIME ==========
void initializeTime() {
  Serial.println("\n3. Synchronizing time...");
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  
  struct tm timeinfo;
  if (getLocalTime(&timeinfo)) {
    Serial.println("   ✅ Time synchronized!");
    Serial.print("   Current time: ");
    Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
  } else {
    Serial.println("   ⚠️  Time sync failed (continuing anyway)");
  }
}

// ========== PROCESS FINGERPRINT SCAN ==========
void processFingerprintScan() {
  // Convert image to template
  Serial.println("   Converting image...");
  uint8_t result = finger.image2Tz();
  
  if (result != FINGERPRINT_OK) {
    Serial.println("   ❌ Error converting image");
    return;
  }
  
  // Search for match
  Serial.println("   Searching for match...");
  result = finger.fingerSearch();
  
  if (result == FINGERPRINT_OK) {
    // Match found!
    Serial.println("   ✅ Match found!");
    Serial.print("   Fingerprint ID: ");
    Serial.print(finger.fingerID);
    Serial.print(" | Confidence: ");
    Serial.println(finger.confidence);
    
    // Mark attendance in Firestore
    if (wifiConnected) {
      markAttendanceInFirestore(finger.fingerID, finger.confidence);
    } else {
      Serial.println("   ⚠️  No WiFi connection - cannot mark attendance");
    }
    
  } else if (result == FINGERPRINT_NOTFOUND) {
    Serial.println("   ❌ No match found");
    Serial.println("   Fingerprint not enrolled in sensor");
  } else {
    Serial.println("   ❌ Error during search");
  }
  
  Serial.println("─────────────────────────────────────────");
}

// ========== MARK ATTENDANCE IN FIRESTORE ==========
void markAttendanceInFirestore(int fingerprintID, int confidence) {
  Serial.println("\n   📡 Marking attendance in Firestore...");
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("   ❌ WiFi disconnected");
    return;
  }
  
  HTTPClient http;
  
  // Step 1: Get student ID from fingerprint mapping
  Serial.println("   1. Looking up student ID...");
  String mappingUrl = FIRESTORE_BASE_URL + "fingerprint_mapping/" + 
                      String(fingerprintID) + "?key=" + FIREBASE_API_KEY;
  
  http.begin(mappingUrl);
  int httpCode = http.GET();
  
  String studentID = "";
  
  if (httpCode == 200) {
    String response = http.getString();
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, response);
    
    if (doc.containsKey("fields") && doc["fields"].containsKey("student_id")) {
      studentID = doc["fields"]["student_id"]["stringValue"].as<String>();
      Serial.print("      Student ID: ");
      Serial.println(studentID);
    } else {
      Serial.println("      ❌ Fingerprint not mapped!");
      Serial.print("      Map it in Firestore: fingerprint_mapping/");
      Serial.println(fingerprintID);
      http.end();
      return;
    }
  } else {
    Serial.println("      ❌ Fingerprint mapping not found!");
    http.end();
    return;
  }
  
  http.end();
  
  // Step 2: Get student details
  Serial.println("   2. Getting student details...");
  String studentUrl = FIRESTORE_BASE_URL + "students/" + studentID + "?key=" + FIREBASE_API_KEY;
  
  http.begin(studentUrl);
  httpCode = http.GET();
  
  String fullName = "";
  String courseCode = "";
  
  if (httpCode == 200) {
    String response = http.getString();
    DynamicJsonDocument doc(2048);
    deserializeJson(doc, response);
    
    if (doc.containsKey("fields")) {
      fullName = doc["fields"]["full_name"]["stringValue"].as<String>();
      courseCode = doc["fields"]["course_code"]["stringValue"].as<String>();
      
      Serial.print("      Name: ");
      Serial.println(fullName);
      Serial.print("      Course: ");
      Serial.println(courseCode);
    }
  } else {
    Serial.println("      ❌ Student not found!");
    http.end();
    return;
  }
  
  http.end();
  
  // Step 3: Check if already marked today
  String today = getCurrentDate();
  String attendanceDocId = studentID + "_" + today + "_" + courseCode;
  
  Serial.println("   3. Checking if already marked...");
  String checkUrl = FIRESTORE_BASE_URL + "attendance/" + attendanceDocId + "?key=" + FIREBASE_API_KEY;
  
  http.begin(checkUrl);
  httpCode = http.GET();
  
  if (httpCode == 200) {
    Serial.println("      ⚠️  Attendance already marked today!");
    
    String response = http.getString();
    DynamicJsonDocument doc(2048);
    deserializeJson(doc, response);
    
    if (doc.containsKey("fields") && doc["fields"].containsKey("time")) {
      String timeMarked = doc["fields"]["time"]["stringValue"].as<String>();
      Serial.print("      Time: ");
      Serial.println(timeMarked);
    }
    
    // Still show welcome message
    Serial.println("\n   ╔══════════════════════════════════════╗");
    Serial.print("   ║ Welcome back, ");
    Serial.print(fullName);
    for(int i = fullName.length(); i < 22; i++) Serial.print(" ");
    Serial.println("║");
    Serial.println("   ║ Already marked today                 ║");
    Serial.println("   ╚══════════════════════════════════════╝");
    
    http.end();
    return;
  }
  
  http.end();
  
  // Step 4: Create attendance record
  Serial.println("   4. Creating attendance record...");
  
  String timestamp = getCurrentTimestamp();
  String timeOnly = getCurrentTime();
  
  // Build Firestore document in JSON format
  DynamicJsonDocument attendanceDoc(2048);
  
  attendanceDoc["fields"]["student_id"]["stringValue"] = studentID;
  attendanceDoc["fields"]["student_name"]["stringValue"] = fullName;
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
  String createUrl = FIRESTORE_BASE_URL + "attendance?documentId=" + attendanceDocId + "&key=" + FIREBASE_API_KEY;
  
  http.begin(createUrl);
  http.addHeader("Content-Type", "application/json");
  
  httpCode = http.POST(jsonPayload);
  
  if (httpCode == 200 || httpCode == 201) {
    Serial.println("      ✅ Attendance marked successfully!");
    
    // Display success message
    Serial.println("\n   ╔══════════════════════════════════════╗");
    Serial.print("   ║ ✅ Welcome, ");
    Serial.print(fullName);
    for(int i = fullName.length(); i < 26; i++) Serial.print(" ");
    Serial.println("║");
    Serial.print("   ║ 📚 Course: ");
    Serial.print(courseCode);
    for(int i = courseCode.length(); i < 26; i++) Serial.print(" ");
    Serial.println("║");
    Serial.print("   ║ 🕐 Time: ");
    Serial.print(timeOnly);
    for(int i = timeOnly.length(); i < 28; i++) Serial.print(" ");
    Serial.println("║");
    Serial.println("   ╚══════════════════════════════════════╝");
    
  } else {
    Serial.println("      ❌ Failed to mark attendance!");
    Serial.print("      HTTP Error: ");
    Serial.println(httpCode);
    Serial.println(http.getString());
  }
  
  http.end();
}

// ========== GET CURRENT DATE (YYYY-MM-DD) ==========
String getCurrentDate() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "2025-01-01";  // Fallback
  }
  
  char dateStr[11];
  strftime(dateStr, sizeof(dateStr), "%Y-%m-%d", &timeinfo);
  return String(dateStr);
}

// ========== GET CURRENT TIMESTAMP (ISO 8601) ==========
String getCurrentTimestamp() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "2025-01-01T00:00:00Z";  // Fallback
  }
  
  char timestampStr[25];
  strftime(timestampStr, sizeof(timestampStr), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
  return String(timestampStr);
}

// ========== GET CURRENT TIME (HH:MM:SS) ==========
String getCurrentTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "00:00:00";  // Fallback
  }
  
  char timeStr[9];
  strftime(timeStr, sizeof(timeStr), "%H:%M:%S", &timeinfo);
  return String(timeStr);
}
