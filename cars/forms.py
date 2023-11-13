from django import forms
from .models import Cars
import datetime


class CarsForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['model', 'brand', 'year']
