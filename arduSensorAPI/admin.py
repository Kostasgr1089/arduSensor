from django.contrib import admin
from .models import DeviceToken

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'token', 'created_at')  # Display the created_at field
    search_fields = ('device_id', 'token')
    readonly_fields = ('token', 'created_at')  # Make created_at read-only
    list_filter = ('created_at',)  # Optional: Add a filter for created_at
