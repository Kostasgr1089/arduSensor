from datetime import timedelta

from django.utils.timezone import now

from .models import AlertThreshold
from arduSensorAPI.gmail_service import send_email_oauth2

# Cooldown interval to avoid spamming the same recipient
ALERT_COOLDOWN = timedelta(minutes=15)


def check_alerts(sensor_data):
    """
    Check device-specific thresholds first; if none exist, fall back to global thresholds.
    Send an alert email when any threshold is violated, respecting a cooldown.

    Args:
        sensor_data: A SensorData instance to evaluate against thresholds.
    """
    # Prefer device-specific thresholds; otherwise use global thresholds
    device_thresholds = AlertThreshold.objects.filter(device_id=sensor_data.device_id)
    thresholds = device_thresholds if device_thresholds.exists() else AlertThreshold.objects.filter(device_id__isnull=True)

    for threshold in thresholds:
        send_email = False
        reason = None
        current_time = now()

        # Temperature checks
        if threshold.max_temperature is not None and sensor_data.temperature > threshold.max_temperature:
            send_email = True
            reason = f"Temperature exceeded: {sensor_data.temperature}°C > {threshold.max_temperature}°C"
        elif threshold.min_temperature is not None and sensor_data.temperature < threshold.min_temperature:
            send_email = True
            reason = f"Temperature below: {sensor_data.temperature}°C < {threshold.min_temperature}°C"

        # Humidity checks
        if threshold.max_humidity is not None and sensor_data.humidity > threshold.max_humidity:
            send_email = True
            reason = f"Humidity exceeded: {sensor_data.humidity}% > {threshold.max_humidity}%"
        elif threshold.min_humidity is not None and sensor_data.humidity < threshold.min_humidity:
            send_email = True
            reason = f"Humidity below: {sensor_data.humidity}% < {threshold.min_humidity}%"

        # Only send if conditions are met and cooldown elapsed
        if send_email and (
            not threshold.last_alert_time
            or current_time - threshold.last_alert_time > ALERT_COOLDOWN
        ):
            send_alert_email(threshold, sensor_data)
            threshold.last_alert_time = current_time
            threshold.save(update_fields=["last_alert_time"])
            # For thesis demo purposes: show what happened
            print(f"Alert sent to {threshold.email} for device {sensor_data.device_id}: {reason}")


def send_alert_email(threshold, data):
    """
    Send an email alert when thresholds are exceeded for a given recipient.
    """
    subject = "Alert: Sensor Threshold Exceeded!"
    message = (
        "Dear user,\n\n"
        "The sensor data has exceeded your set threshold.\n\n"
        f"Device ID: {data.device_id}\n"
        f"Temperature: {data.temperature}°C\n"
        f"Humidity: {data.humidity}%\n\n"
        "Please take immediate action!\n\n"
        "Best Regards,\n"
        "arduSensor Monitoring System."
    )
    send_email_oauth2(subject, message, threshold.email)