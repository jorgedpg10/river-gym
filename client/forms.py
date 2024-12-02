from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'dni', 'celphone', 'address', 'observation', 'image', 'active_membership', 'active_until']