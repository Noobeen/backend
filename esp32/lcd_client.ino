#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal.h>
#include <ArduinoJson.h>  // install via Library Manager

/***** USER CONFIG *****/
const char* SSID     = "Galaxy";
const char* PASSWORD = "ayush123";
const char* SERVER   = "http://ip:5000/message";  // e.g. http://192.168.1.37:5000/message
const uint8_t POLL_MS = 5000;  // refresh every 5 s
/************************/

LiquidCrystal lcd(32, 26, 14, 12, 13, 27);
String lastText;

void setup() {
  Serial.begin(115200);
  lcd.begin(16, 2);
  lcd.print("Connecting...");

  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(200); Serial.print('.');
  }
  lcd.clear(); lcd.print("WiFi OK");
  delay(500);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER);
    int code = http.GET();
    if (code == 200) {
      DynamicJsonDocument doc(128);
      deserializeJson(doc, http.getString());
      String txt = doc["text"].as<String>();
      if (txt != lastText) {
        lastText = txt;
        lcd.clear(); lcd.setCursor(0,0); lcd.print(txt);
        Serial.println("[LCD] " + txt);
      }
    }
    http.end();
  }
  delay(POLL_MS);
}