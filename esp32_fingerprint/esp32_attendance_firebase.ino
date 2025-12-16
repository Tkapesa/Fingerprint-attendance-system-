/*
============================================================
ESP32 FINGERPRINT ATTENDANCE SYSTEM WITH FIREBASE
============================================================
Hardware: ESP32 + R307 Fingerprint Sensor
Database: Firebase Realtime Database
Connection: WiFi

Wiring (R307 to ESP32):
- R307 VCC (Red)    → ESP32 3.3V or 5V
- R307 GND (Black)  → ESP32 GND
- R307 TX (White)   → ESP32 RX2 (GPIO 16)
- R307 RX (Green)   → ESP32 TX2 (GPIO 17)

Setup Instructions:
1. Install ESP32 board support in Arduino IDE
2. Install libraries:
   - Firebase ESP32 Client (by Mobizt)
   - Adafruit Fingerprint Sensor Library
3. Update WiFi and Firebase credentials below
4. Upload to ESP32

============================================================
*/

#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Adafruit_Fingerprint.h>
#include <time.h>

// ========== WIFI CONFIGURATION ==========
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ========== FIREBASE CONFIGURATION ==========
// Get from Firebase Console > Project Settings
#define FIREBASE_HOST "attendance-system-xxxxx.firebaseio.com"  // Without https://
#define FIREBASE_AUTH "YOUR_FIREBASE_WEB_API_KEY"

// ========== HARDWARE CONFIGURATION ==========
#define SENSOR_RX 16  // ESP32 GPIO16 → R307 TX
#define SENSOR_TX 17  // ESP32 GPIO17 → R307 RX

// ========== GLOBAL OBJECTS ==========
HardwareSerial fingerprintSerial(2);  // Use UART2
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&fingerprintSerial);

FirebaseData firebaseData;
FirebaseAuth firebaseAuth;
FirebaseConfig firebaseConfig;

// ========== GLOBAL VARIABLES ==========
bool wifiConnected = false;
bool firebaseConnected = false;
unsigned long lastScanTime = 0;
const unsigned long SCAN_COOLDOWN = 3000;  // 3 seconds between scans

// NTP Time Server
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;  // Adjust for your timezone (0 = UTC)
const int daylightOffset_sec = 0;

// ========== SETUP FUNCTION ==========
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n========================================");
  Serial.println("ESP32 FINGERPRINT ATTENDANCE SYSTEM");
  Serial.println("With Firebase Realtime Database");
  Serial.println("========================================\n");
  
  // 1. Initialize Fingerprint Sensor
  initializeSensor();
  
  // 2. Connect to WiFi
  connectWiFi();
  
  // 3. Initialize Time
  if (wifiConnected) {
    initializeTime();
  }
  
  // 4. Connect to Firebase
  if (wifiConnected) {
    connectFirebase();
  }
  
  // 5. System Ready
  Serial.println("\n========================================");
  if (wifiConnected && firebaseConnected) {
    Serial.println("✅ SYSTEM READY!");
    Serial.println("Place finger on sensor to mark attendance");
  } else {
    Serial.println("⚠️  SYSTEM RUNNING IN LIMITED MODE");
    Serial.println("Sensor working but no cloud connection");
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

// ========== CONNECT TO FIREBASE ==========
void connectFirebase() {
  Serial.println("\n4. Connecting to Firebase...");
  
  // Configure Firebase
  firebaseConfig.host = FIREBASE_HOST;
  firebaseConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  
  // Initialize Firebase
  Firebase.begin(&firebaseConfig, &firebaseAuth);
  Firebase.reconnectWiFi(true);
  
  // Test connection
  if (Firebase.ready()) {
    firebaseConnected = true;
    Serial.println("   ✅ Firebase Connected!");
    Serial.print("   Database: ");
    Serial.println(FIREBASE_HOST);
  } else {
    firebaseConnected = false;
    Serial.println("   ❌ Firebase Connection Failed!");
    Serial.println("   Check credentials and database URL");
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
    
    // Mark attendance in Firebase
    if (firebaseConnected) {
      markAttendanceInFirebase(finger.fingerID, finger.confidence);
    } else {
      Serial.println("   ⚠️  No Firebase connection - cannot mark attendance");
    }
    
  } else if (result == FINGERPRINT_NOTFOUND) {
    Serial.println("   ❌ No match found");
    Serial.println("   Fingerprint not enrolled in sensor");
  } else {
    Serial.println("   ❌ Error during search");
  }
  
  Serial.println("─────────────────────────────────────────");
}

// ========== MARK ATTENDANCE IN FIREBASE ==========
void markAttendanceInFirebase(int fingerprintID, int confidence) {
  Serial.println("\n   📡 Marking attendance in Firebase...");
  
  // Step 1: Get student ID from fingerprint mapping
  String mappingPath = "/fingerprint_mapping/" + String(fingerprintID);
  String studentID = "";
  
  Serial.println("   1. Looking up student ID...");
  if (Firebase.getString(firebaseData, mappingPath)) {
    studentID = firebaseData.stringData();
    Serial.print("      Student ID: ");
    Serial.println(studentID);
  } else {
    Serial.println("      ❌ Fingerprint not mapped to any student!");
    Serial.println("      Please map fingerprint in Firebase:");
    Serial.print("      /fingerprint_mapping/");
    Serial.print(fingerprintID);
    Serial.println(" = \"ST001\"");
    return;
  }
  
  // Step 2: Get student details
  Serial.println("   2. Getting student details...");
  String studentPath = "/students/" + studentID;
  
  if (!Firebase.get(firebaseData, studentPath)) {
    Serial.println("      ❌ Student not found in database!");
    return;
  }
  
  FirebaseJson studentJson = firebaseData.jsonObject();
  String fullName = "";
  String courseCode = "";
  
  studentJson.get(firebaseData, "full_name");
  fullName = firebaseData.stringData();
  
  studentJson.get(firebaseData, "course_code");
  courseCode = firebaseData.stringData();
  
  Serial.print("      Name: ");
  Serial.println(fullName);
  Serial.print("      Course: ");
  Serial.println(courseCode);
  
  // Step 3: Check if already marked today
  String today = getCurrentDate();
  String attendancePath = "/attendance/" + today + "/" + courseCode + "/" + studentID;
  
  Serial.println("   3. Checking if already marked...");
  if (Firebase.get(firebaseData, attendancePath)) {
    if (!firebaseData.jsonObject().isnull()) {
      Serial.println("      ⚠️  Attendance already marked today!");
      
      // Get time marked
      firebaseData.jsonObject().get(firebaseData, "time");
      String timeMarked = firebaseData.stringData();
      
      Serial.print("      Time: ");
      Serial.println(timeMarked);
      
      // Still show success message
      Serial.println("\n   ╔══════════════════════════════════════╗");
      Serial.print("   ║ Welcome back, ");
      Serial.print(fullName);
      for(int i = fullName.length(); i < 22; i++) Serial.print(" ");
      Serial.println("║");
      Serial.print("   ║ Already marked at ");
      Serial.print(timeMarked);
      for(int i = timeMarked.length(); i < 18; i++) Serial.print(" ");
      Serial.println("║");
      Serial.println("   ╚══════════════════════════════════════╝");
      return;
    }
  }
  
  // Step 4: Create attendance record
  Serial.println("   4. Creating attendance record...");
  
  String timestamp = getCurrentTimestamp();
  String timeOnly = getCurrentTime();
  
  FirebaseJson attendanceJson;
  attendanceJson.set("student_name", fullName);
  attendanceJson.set("student_id", studentID);
  attendanceJson.set("course_code", courseCode);
  attendanceJson.set("timestamp", timestamp);
  attendanceJson.set("time", timeOnly);
  attendanceJson.set("status", "present");
  attendanceJson.set("scan_method", "fingerprint");
  attendanceJson.set("fingerprint_id", fingerprintID);
  attendanceJson.set("confidence", confidence);
  
  if (Firebase.setJSON(firebaseData, attendancePath, attendanceJson)) {
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
    Serial.print("      Error: ");
    Serial.println(firebaseData.errorReason());
  }
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
