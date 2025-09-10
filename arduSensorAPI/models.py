from django.db import models
import uuid

class DeviceToken(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) #track when the token was created

    def __str__(self):
        return self.device_id

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    device_id = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id} - Temp: {self.temperature}, Humidity: {self.humidity}, Created: {self.created_at}"


class AlertThreshold(models.Model):
    device_id = models.CharField(max_length=100, null=True, blank=True)  
    max_temperature = models.FloatField(null=True, blank=True)
    min_temperature = models.FloatField(null=True, blank=True)
    max_humidity = models.FloatField(null=True, blank=True)
    min_humidity = models.FloatField(null=True, blank=True)
    email = models.EmailField()  # Email to send alerts to
    last_alert_time = models.DateTimeField(null=True, blank=True)  # Track when the last alert was sent

    def __str__(self):
        return f"Threshold for device {self.device_id or 'Global'}"
