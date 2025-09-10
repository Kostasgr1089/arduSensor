import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from arduSensorAPI.forms import ThresholdForm
from .models import AlertThreshold, DeviceToken, SensorData
from .serializers import SensorDataSerializer
from rest_framework import views, status
from rest_framework.response import Response
from django.utils import timezone
from django.utils.timezone import now, localtime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .alerts import check_alerts  
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import SensorData
from .serializers import SensorDataSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny



def base(request):
    return HttpResponse("Welcome to the Sensor Data API!")




# Enhanced View for handling sensor data via API
@method_decorator(login_required, name='dispatch')
class SensorDataView(views.APIView):
    def get(self, request, *args, **kwargs):
        # Fetch data from the last 5 minutes (or specify another timeframe)
        since_time = now() - timedelta(minutes=5)
        data = SensorData.objects.filter(created_at__gte=since_time)
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def history_view(request):
    device_ids = SensorData.objects.values_list('device_id', flat=True).distinct()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        selected_device = request.GET.get('device', 'all')
        interval = request.GET.get('interval', '1d')
        now = timezone.now()

        # Define time intervals
        if interval == '1d':
            start_time = now - timedelta(days=1)
        elif interval == '1w':
            start_time = now - timedelta(weeks=1)
        elif interval == '1m':
            start_time = now - timedelta(weeks=4)
        elif interval == '1y':
            start_time = now - timedelta(weeks=52)
        else:
            start_time = None

        # Filter data by device and time
        if start_time:
            if selected_device == 'all':
                data = SensorData.objects.filter(created_at__gte=start_time).order_by('-created_at')
            else:
                data = SensorData.objects.filter(device_id=selected_device, created_at__gte=start_time).order_by('-created_at')
        else:
            data = SensorData.objects.all().order_by('-created_at') if selected_device == 'all' else SensorData.objects.filter(device_id=selected_device).order_by('-created_at')

        temperatures = [reading.temperature for reading in data]
        humidities = [reading.humidity for reading in data]
        timestamps = [localtime(reading.created_at).strftime("%Y-%m-%d %H:%M:%S") for reading in data]

        return JsonResponse({
            'temperatures': temperatures,
            'humidities': humidities,
            'timestamps': timestamps,
            'device_ids': list(device_ids),
            'selected_device': selected_device,
        })

    # For normal requests, render the 'history.html' page
    return render(request, 'history.html', {'device_ids': device_ids, 'selected_device': 'all'})



@login_required
def display_data(request):
    """
    Handles both rendering the dashboard and returning JSON data for charts.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        device = request.GET.get('device', 'all')
        two_hours_ago = now() - timedelta(hours=2)

        if device == 'all':
            data = SensorData.objects.filter(created_at__gte=two_hours_ago).order_by('-created_at')
        else:
            data = SensorData.objects.filter(device_id=device, created_at__gte=two_hours_ago).order_by('-created_at')

        response_data = [
            {
                'created_at': localtime(entry.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': entry.temperature,
                'humidity': entry.humidity,
                'device_id': entry.device_id
            }
            for entry in data
        ]
        return JsonResponse(response_data, safe=False)

    # Handle normal request and render the HTML dashboard
    device_ids = SensorData.objects.values_list('device_id', flat=True).distinct()
    return render(request, 'display_data.html', {'device_ids': device_ids})


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])  #No TokenAuthentication for this endpoint
@permission_classes([AllowAny])  #Allow anyone to hit this, we will verify manually
def sensor_data(request):
    if request.method == 'POST':
        # Your existing manual device token validation
        auth_token = request.headers.get('Authorization')
        if not auth_token or not DeviceToken.objects.filter(token=auth_token).exists():
            return JsonResponse({"error": "Unauthorized"}, status=401)

        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))
        device_id = request.POST.get('device_id') or 'unknown'

        new_data = SensorData.objects.create(
            temperature=temperature,
            humidity=humidity,
            device_id=device_id
        )

        check_alerts(new_data)

        return JsonResponse({"success": True, "message": "Data received successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def settings_view(request):
    # Fetch distinct device IDs from the SensorData model
    device_ids = SensorData.objects.values_list('device_id', flat=True).distinct()

    if request.method == 'POST':
        # Create a new threshold without overwriting existing ones
        form = ThresholdForm(request.POST)
        if form.is_valid():
            device_id = request.POST.get('device_id') or None  # Get device_id or set it to None for global
            email = form.cleaned_data['email']
            
            # Check if a threshold with the same device_id and email already exists
            if AlertThreshold.objects.filter(device_id=device_id, email=email).exists():
                form.add_error(None, "A threshold with this email and device already exists.")
            else:
                AlertThreshold.objects.create(
                    device_id=device_id,
                    max_temperature=form.cleaned_data['max_temperature'],
                    min_temperature=form.cleaned_data['min_temperature'],
                    max_humidity=form.cleaned_data['max_humidity'],
                    min_humidity=form.cleaned_data['min_humidity'],
                    email=email
                )
                return redirect('settings')
    else:
        form = ThresholdForm()

    # Fetch all existing thresholds to display in the table
    existing_thresholds = AlertThreshold.objects.all()

    return render(request, 'settings.html', {
        'form': form,
        'existing_thresholds': existing_thresholds,
        'device_ids': device_ids,
    })


def base_view(request):
    dark_mode = request.COOKIES.get('darkMode') == 'enabled'
    return render(request, 'base.html', {'dark_mode': dark_mode})

@login_required
def delete_threshold(request, threshold_id):
    threshold = get_object_or_404(AlertThreshold, id=threshold_id)
    threshold.delete()
    return HttpResponseRedirect(reverse('settings'))


@login_required
def exportSensorDataCSV(request):
    device_id = request.GET.get('device_id', 'all')
    interval = request.GET.get('interval', 'all')
    now_time = timezone.now()

    if interval == '1d':
        start_time = now_time - timedelta(days=1)
    elif interval == '1w':
        start_time = now_time - timedelta(weeks=1)
    elif interval == '1m':
        start_time = now_time - timedelta(weeks=4)
    elif interval == '1y':
        start_time = now_time - timedelta(weeks=52)
    else:
        start_time = None  # For 'all' case

    queryset = SensorData.objects.all()
    if device_id != 'all':
        queryset = queryset.filter(device_id=device_id)
    if start_time:
        queryset = queryset.filter(created_at__gte=start_time)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensor_data_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Temperature', 'Humidity', 'Device ID', 'Created At'])
    for data in queryset:
        writer.writerow([data.temperature, data.humidity, data.device_id, localtime(data.created_at).strftime("%Y-%m-%d %H:%M:%S")])

    return response


class ExportSensorDataJSONView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]  #Allow both
    permission_classes = [IsAuthenticated]  #User must be authenticated (either token OR login)

    def get(self, request, *args, **kwargs):
        device_id = request.GET.get('device_id', 'all').strip()
        interval = request.GET.get('interval', 'all').strip()

        interval_mapping = {
            '1d': timezone.now() - timedelta(days=1),
            '1w': timezone.now() - timedelta(weeks=1),
            '1m': timezone.now() - timedelta(weeks=4),
            '1y': timezone.now() - timedelta(weeks=52),
            'all': None
        }

        if interval not in interval_mapping.keys():
            return Response(
                {"error": "Invalid interval parameter. Must be one of: 1d, 1w, 1m, 1y, all."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = SensorData.objects.all()

        if device_id != 'all':
            queryset = queryset.filter(device_id=device_id)
        if interval_mapping[interval]:
            queryset = queryset.filter(created_at__gte=interval_mapping[interval])

        serializer = SensorDataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)