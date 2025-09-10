from django.core.management.base import BaseCommand
from arduSensorAPI.models import DeviceToken

class Command(BaseCommand):
    help = 'Create or retrieve a device token for a given device_id.'

    def add_arguments(self, parser):
        parser.add_argument('device_id', type=str, help='The device ID for which to create or retrieve the token.')

    def handle(self, *args, **kwargs):
        device_id = kwargs['device_id']
        device_token, created = DeviceToken.objects.get_or_create(device_id=device_id)

        if created:
            self.stdout.write(self.style.SUCCESS(f"New token created for device '{device_id}': {device_token.token}"))
        else:
            self.stdout.write(self.style.WARNING(f"Existing token for device '{device_id}': {device_token.token}"))
