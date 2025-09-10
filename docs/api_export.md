# 📜 How to Export Sensor Data via API (JSON)

This guide explains how to **authenticate** and **request sensor data exports** through the protected **JSON API endpoint**.

---

## 1. 📦 API Requirements

Before you can export data, ensure:

* You have a valid **API Token** linked to your Django User.
* You know the **base URL** of the API server (e.g., `https://yourdomain.com/`).

If you don't have a token yet, refer to the [User Token Creation Guide](#) to create one.

---

## 2. 🔑 Authentication

All requests must include a valid **Authorization Token** in the HTTP headers.

Example:

```http
Authorization: Token your_generated_token_here
```

Without a valid token, the server will reject the request with a `403 Forbidden` error.

---

## 3. 📬 API Endpoint Details

| Field               | Value                         |
| ------------------- | ----------------------------- |
| **URL**             | `/export-data-json/`          |
| **Method**          | `GET`                         |
| **Authentication**  | Token Authentication (Header) |
| **Response Format** | JSON array                    |

---

## 4. 🔎 Supported Query Parameters

You can filter the data export using the following optional parameters:

| Parameter   | Required | Description                                         | Example              |
| ----------- | -------- | --------------------------------------------------- | -------------------- |
| `device_id` | Optional | Filter by device ID (e.g., `sensor01`)              | `device_id=sensor01` |
| `interval`  | Optional | Time range to export: `1d`, `1w`, `1m`, `1y`, `all` | `interval=1w`        |

* `1d` → Last day
* `1w` → Last week
* `1m` → Last month
* `1y` → Last year
* `all` → All available data

If no parameters are provided, the system exports **all sensor data**.

---

## 5. 🚀 Example Requests

### Basic Example (All Data)

```bash
curl -H "Authorization: Token your_token_here" "https://yourdomain.com/export-data-json/"
```

### Export Data for a Specific Device Over the Last Week

```bash
curl -H "Authorization: Token your_token_here" "https://yourdomain.com/export-data-json/?device_id=sensor01&interval=1w"
```

### Export Last Day's Data for All Devices

```bash
curl -H "Authorization: Token your_token_here" "https://yourdomain.com/export-data-json/?interval=1d"
```

### Example in Python (using `requests` library)

```python
import requests

url = "https://yourdomain.com/export-data-json/"
headers = {
    'Authorization': 'Token your_token_here'
}
params = {
    'device_id': 'sensor01',
    'interval': '1w'
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
```

---

## 6. 📦 Example API Response

```json
[
  {
    "temperature": 24.5,
    "humidity": 60.2,
    "device_id": "sensor01",
    "created_at": "2025-05-10T14:35:12Z"
  },
  {
    "temperature": 25.1,
    "humidity": 61.0,
    "device_id": "sensor01",
    "created_at": "2025-05-10T15:15:09Z"
  }
]
```

---

## 7. ⚠️ Common Errors

| Error             | Meaning                                        | Solution                                                  |
| ----------------- | ---------------------------------------------- | --------------------------------------------------------- |
| `403 Forbidden`   | Missing or invalid token                       | Make sure the Authorization header includes a valid token |
| `400 Bad Request` | Invalid query parameter (e.g., wrong interval) | Use only allowed intervals: `1d`, `1w`, `1m`, `1y`, `all` |

---

# 🏁 Done!

You are now ready to securely export your **Sensor Data** through the **protected JSON API endpoint**.

Make sure to keep your **API Token safe** and rotate it periodically for security best practices.
