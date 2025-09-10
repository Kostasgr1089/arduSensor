import os
import django

# Set DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Replace 'myproject' with your actual project name

django.setup()

from arduSensorAPI.models import DeviceToken  # Import after django.setup()



def create_device_token():
    # Prompt the user for the device name
    device_id = input("Enter the device name: ").strip()

    # Check if a token already exists for this device
    device_token, created = DeviceToken.objects.get_or_create(device_id=device_id)
    
    if created:
        print(f"New token created for device '{device_id}': {device_token.token}")
    else:
        print(f"Existing token for device '{device_id}': {device_token.token}")
    
    return device_token.token

if __name__ == "__main__":
    create_device_token()
