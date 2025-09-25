#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include "DHT20.h"

// Network credentials
const char* ssid = "your_WiFi_SSID_Here";
const char* password = "Your_WiFi_Pass_Here";

// Arduino Identifier
String device_id = "ESP8266";

// Server URL
const char* serverUrl = "http://server_IP:8000/api/sensor_data_post/";

// Token for authentication
const char* authToken = "eee71bb7-aa69-4f49-9768-4439085efc36";  // Replace with your actual token

// Initialize the DHT20
DHT20 DHT;

WiFiClient client;  // Create a WiFi client

void setup() {
  Serial.begin(115200);
  Serial.println(__FILE__);
  Serial.print("DHT20 LIBRARY VERSION: ");
  Serial.println(DHT20_LIB_VERSION);

  // Initialize I2C
  Wire.begin();
  // Initialize the DHT20 sensor
  DHT.begin();

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(1000);
}

void loop() {
  if (millis() - DHT.lastRead() >= 30000) {  // Read every 30 seconds
    int status = DHT.read();
    if (status == DHT20_OK) {
      // Prepare data string
      String httpRequestData = "temperature=" + String(DHT.getTemperature()) 
                             + "&humidity=" + String(DHT.getHumidity()) 
                             + "&device_id=" + String(device_id);

      // Send data to server
      HTTPClient http;
      http.begin(client, serverUrl);  // Pass the WiFi client and URL
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      http.addHeader("Authorization", String(authToken));  // Add token to header

      int httpResponseCode = http.POST(httpRequestData);
      Serial.println("HTTP Request Data:");
      Serial.println(httpRequestData);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("HTTP Response code: " + String(httpResponseCode));
        Serial.println("Response: " + response);
      } else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
      }

      http.end();
    } else {
      Serial.println("Failed to read data from sensor!");
    }
  }
}
