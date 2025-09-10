# 🌐 ArduSensor Monitoring System

Welcome to the **ArduSensor** project!  
This is my undergraduate **thesis project** at **Harokopio University of Athens (Department of Informatics and Telematics)**.  

ArduSensor is a condition monitoring system for a Data Center using Python/Django and microcontrollers. Providing a user-friendly UI, the ability to monitor data, view data historically, set thresholds for email alerts and export stored data on JSON and CSV files

---

👉 For full installation and configuration instructions, see [SETUP.md](SETUP.md).  
👉 For microcontroller setup, see [arduinoSetup.md](arduinoSetup.md).  



## 🔍 Project Overview

**Features:**

* Real-time sensor data collection from IoT devices.
* Threshold management with email alerts.
* Data visualization via web dashboard.
* Secure API endpoints for data export (CSV, JSON).
* Dual authentication system: **Web Login** and **API Token Authentication**.
* Dark mode UI support for better user experience.

---

## 🛡️ Security Overview

| Access Type                      | Authentication Method                         | Notes                                      |
| :------------------------------- | :-------------------------------------------- | :----------------------------------------- |
| Web Pages (settings, dashboard)  | `@login_required` (Django session)            | Browser-based access only.                 |
| API Endpoints (JSON, CSV Export) | Token Authentication + Session Authentication | API clients and logged-in users supported. |
| IoT Devices                      | Custom DeviceToken system                     | Token tied to each device ID.              |
  
* API clients authenticate using Django REST Framework **User Tokens**.

---

## 🔢 Main Technologies Used

* **Backend**: Django 5.x, Django REST Framework
* **Frontend**: HTML5, Bootstrap 5, basic JavaScript
* **Database**: PostgreSQL
* **Other**: Django Email System (OAuth-secured Gmail alerts)

---

## 📂 Folder Structure

```bash
arduSensor/
├── manage.py
├── arduSensor/        # core project settings
├── arduSensorAPI/     # main app (models, views, serializers, commands)
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│   ├── forms.py
│   ├── templates/
│   └── management/commands/   # custom shell commands
├── requirements.txt
├── example_data.json  # demo dataset
├── SETUP.md           # detailed setup guide
└── arduinoSetup.md    # Arduno / ESP setup guide

```

---

### 1. Access Web Page UI

1. Start the server.

```python manage.py runserver```
Local access: http://127.0.0.1:8000
By default, it will start at:
Local access: http://127.0.0.1:8000 or http://localhost:8000

Network access: http://<server-ip>:8000
 (replace <server-ip> with your machine’s IP if you want to connect from another device on the same network).
2. Login with your superuser or user credentials

For admin-level management visit:

http://<server-ip>:8000/admin/

Once logged in, you can:
1. Access the dashboard with the realtime sensor readings.
2. Access the history tab to view the readings stored in the database.
3. Manage alert thresholds through the settings tab.
4. Export data through the settings tab.
   
---

### 2. Post Data Without a Device (CLI)

You can simulate the ESP by sending an HTTP POST to the same endpoint your microcontroller uses:

POST /api/sensor_data_post/ with Content-Type: application/x-www-form-urlencoded and a DeviceToken in the Authorization header.

0. Prerequisite
   
Create a DeviceToken

```
python manage.py createDeviceToken demo-esp
```

→ copy the printed token, e.g. 11111111-2222-3333-4444-555555555555

2. Using curl (Linux/macOS)
```
curl -X POST "http://<server-ip>:8000/api/sensor_data_post/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: 11111111-2222-3333-4444-555555555555" \
  --data "temperature=24.5&humidity=53.2&device_id=demo-esp"
```

2. Using curl (Windows PowerShell)

```
curl.exe -X POST "http://<server-ip>:8000/api/sensor_data_post/" `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -H "Authorization: 11111111-2222-3333-4444-555555555555" `
  --data "temperature=24.5&humidity=53.2&device_id=demo-esp"
```

3. Using Postman
   1. Method: POST
   2. URL: http://<server-ip>:8000/api/sensor_data_post/
   3. Headers: Authorization: 11111111-2222-3333-4444-555555555555 Content-Type: application/x-www-form-urlencoded
   4. Body: temperature=24.5&humidity=53.2&device_id=demo-esp
  
---

### 3. Export Sensor Data (JSON)

* URL: `http://localhost:8000/api/export-data-json/`
* Method: `GET`
* Headers:

  * `Authorization: Token your_token_here`
* Optional Parameters:

  * `device_id`
  * `interval` (`1d`, `1w`, `1m`, `1y`, `all`)

Example `curl`:

```bash
curl -H "Authorization: Token your_token_here" "http://localhost:8000/api/export-data-json/?device_id=sensor01&interval=1w"
```

---

## Web Dashboard Access

* Login at: `http://localhost:8000/accounts/login/`
* Manage thresholds, view sensor data history, export data manually.

---

## Demo Dataset

A demo dataset (example_data.json) is included for testing.
See SETUP.md – Using Example Data
 for instructions on how to load it.
 
---

## Credits

Project developed by: Konstantinos Gerokostas

Institution: Harokopio University of Athens, Department of Informatics and Telematics
Special Thanks: Django, Django REST Framework, and the open-source community.

This repository contains the full source code of my undergraduate thesis project.
