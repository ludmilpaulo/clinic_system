# forms.py
from django import forms
from .models import Image
from .widgets import MultipleFileInput

class MultipleImageUploadForm(forms.Form):
    images = forms.FileField(widget=MultipleFileInput())
