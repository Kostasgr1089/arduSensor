from django.urls import path
from .views import (
    SensorDataView,
    display_data,
    sensor_data,
    delete_threshold,
    exportSensorDataCSV,
    ExportSensorDataJSONView,
)
from arduSensorAPI import views

urlpatterns = [
    path('sensor_data_post/', sensor_data, name='sensor_data_post'),  # Endpoint for POST requests from devices
    path('sensor_data/', SensorDataView.as_view(), name='sensor_data'),  # Endpoint for other API interactions
    path('history/', views.history_view, name='history'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/delete/<int:threshold_id>/', delete_threshold, name='delete_threshold'),
    path('display-data/', display_data, name='display_data'),

    # --- New Export Endpoints ---
    path('export-data-csv/', exportSensorDataCSV, name='export_sensor_data_csv'),  # CSV Export
    path('export-data-json/', ExportSensorDataJSONView.as_view(), name='export_sensor_data_json'),  # JSON Export
]
