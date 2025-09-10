# ArduSensor – Setup Guide

This guide explains how to install, configure, and run the **ArduSensor** project, including the backend (Django + PostgreSQL), the development board token, Gmail alerts.

---

## 1. Requirements

- Python 3.10+
- PostgreSQL 14+
- Git
- Arduino IDE 

---

## 2. Clone and Environment Setup

```bash
git clone https://github.com/<your-username>/arduSensor.git
cd arduSensor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Database Setup
   
Create the database

```sql
CREATE DATABASE ardu_sensor;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE ardu_sensor TO postgres;

```
Apply migrations
```
python manage.py migrate
```
Create an admin user
```
python manage.py createsuperuser
```

You will be prompted to enter:

Username

Email address

Password

---

## 4. Device Tokens

Each device must have a DeviceToken in order to send temperature and humidity data.

Create a device token

```
python manage.py createDeviceToken <device_id>
```

You must use the same device_id as well as copy the token from the terminal window onto your arduino code 

```c#
String device_id = "ESP8266";   // or another identifier
const char* authToken = "<your-token>";   // token
```

You can also manipulate deviceTokens straight from the Admin panel in localhost:8000/Admin

👉 For the full development board setup (Configuration, libraries, wiring, and uploading), see [arduinoSetup.md](arduinoSetup.md).
