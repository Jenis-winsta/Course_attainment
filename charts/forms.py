# forms.py
from django import forms
from .models import *
from django.core.exceptions import ValidationError


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Select an Excel file')
    year = forms.ModelChoiceField(queryset=File_Description.objects.all())

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.xlsx'):
            raise ValidationError('Only .xlsx files are allowed.')
        return file                                                                                            