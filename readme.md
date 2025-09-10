# 🌐 ArduSensor Monitoring System

Welcome to the **ArduSensor** project! This Django-based system is designed for monitoring IoT sensor data securely and flexibly, with both a user-friendly web interface and a professional REST API.

---

👉 For full installation and configuration instructions, see [SETUP.md](SETUP.md).  
👉 For microcontroller setup, see [arduinoSetup.md](arduinoSetup.md).  
👉 For loading demo data, see [SETUP.md – Using Example Data](SETUP.md#6-using-example-data).


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

* IoT devices authenticate using a custom **DeviceToken** system.
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
myproject/
├── manage.py
├── myproject/ (core project settings)
└── myapi/ (main app)
    ├── views.py
    ├── models.py
    ├── serializers.py
    ├── forms.py
    ├── templates/
    └── management/commands/ (custom shell scripts)
```

---

## 📊 API Usage Instructions

### 1. Obtain an API Token

* Create a Django user:

```bash
python manage.py createsuperuser
```

* Generate a Token for the user:

```bash
python manage.py createUserToken <username>
```

### 2. Export Sensor Data (JSON)

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

## 📃 Web Dashboard Access

* Login at: `http://localhost:8000/accounts/login/`
* Manage thresholds, view sensor data history, export data manually.

---

## 💪 Credits

**Project developed by**: K. Gerokostas

**Special Thanks**: Everyone contributing to Django, Django REST Framework, and the open-source community.

---

# 🚀 Let's monitor smart, let's monitor safe!

