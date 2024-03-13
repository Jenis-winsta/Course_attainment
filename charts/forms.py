from django import forms
from .models import Student

class UploadFileForm(forms.Form):
    file= forms.FileField(label='Select an Excel file')