from django import forms
from .models import AlertThreshold

class ThresholdForm(forms.ModelForm):
    class Meta:
        model = AlertThreshold
        fields = ['max_temperature', 'min_temperature', 'max_humidity', 'min_humidity', 'email']
        widgets = {
            'max_temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Max Temperature'}),
            'min_temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Min Temperature'}),
            'max_humidity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Max Humidity'}),
            'min_humidity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Min Humidity'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Recipient\'s Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required
        for field in self.fields.values():
            field.required = True
