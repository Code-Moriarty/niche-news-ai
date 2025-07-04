from django import forms
from .models import Niche

class NicheForm(forms.ModelForm):
    class Meta:
        model = Niche
        fields = ['name']
