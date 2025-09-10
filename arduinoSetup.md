# Arduino / ESP Firmware Setup

This firmware reads temperature and humidity from a **DHT20** sensor and sends it to the ArduSensor backend over Wi-Fi.  
It can be adapted for ESP8266, ESP32 or other development boards, this project uses an **ESP8266**.

---

## 1. Requirements

- **Arduino IDE** (latest version)  
- **ESP8266 Core** installed  
- **DHT20 library** installed  

---

## 2. Install Board Support

1. Open **Arduino IDE**.  
2. Go to *File → Preferences → Additional Boards Manager URLs* and add:  

https://arduino.esp8266.com/stable/package_esp8266com_index.json

3. Go to *Tools → Board → Boards Manager…*, search for **esp8266**, and install the **ESP8266 Core**.

 ---

## 3. Install the DHT20 Library

- Go to *Sketch → Include Library → Manage Libraries…*  
- Search for **DHT20** (e.g., by Rob Tillaart) and install.  

---

## 4. Hardware Wiring

| ESP8266 Pin | DHT20 Pin |
|-------------|-----------|
| 3V3         | VCC       |
| GND         | GND       |
| D2 (GPIO4)  | SDA       |
| D1 (GPIO5)  | SCL       |

---

## 5. Configure the Firmware

Edit the sketch and set:

```cpp
const char* ssid = "YourWiFiSSID";
const char* password = "YourWiFiPassword";


String device_id = "ESP8266";
const char* serverUrl = "http://<server-ip>:8000/api/sensor_data_post/";
const char* authToken = "<device-token>";

```

---

# 6. Upload and Run

1. Tools → board → Select your development board (e.g., NodeMCU 1.0).
2. Tools → Port → Select the correct COM port.
3. Click Upload.
4. Open Serial Monitor at 115200 baud to see log.

Every ~30 seconds you should see POST requests like:

```ini
temperature=24.10&humidity=52.40&device_id=ESP8266
```

---

# 7. Troubleshooting

1. No WiFi connection: Check SSID/Password.
2. Failed to read data from sensor: Check SDA/SCL wiring.
3. HTTP errors: Verify serverUrl and authToken. 
