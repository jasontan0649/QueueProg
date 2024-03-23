# queue_app/forms.py
from django import forms
from .models import QueueNumber

class QueueNumberForm(forms.ModelForm):
    class Meta:
        model = QueueNumber
        fields = ['message']  # Assuming 'message' is the only field you want from the user
