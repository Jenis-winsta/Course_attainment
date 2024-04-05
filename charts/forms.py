# forms.py
from django import forms
from .models import *
from django.core.exceptions import ValidationError
<<<<<<< HEAD


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Select an Excel file')
    year = forms.ModelChoiceField(queryset=File_Description.objects.all())

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.xlsx'):
            raise ValidationError('Only .xlsx files are allowed.')
        return file                                                                                            
=======
from techapp.models import *

'''
class UploadForm(forms.Form):
    file = forms.FileField(label='Select an Excel file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'] = forms.ModelChoiceField(queryset=File_Description.objects.values_list('year', flat=True).distinct())
        self.fields['course_code'] = forms.ModelChoiceField(queryset=Course.objects.values_list('course_code', flat=True).distinct())

    def clean(self):
        cleaned_data = super().clean()
        file = self.cleaned_data['file']
        # course_code = cleaned_data.get('course_code')

        if not file.name.endswith(('.xlsx', 'xls')):
            raise forms.ValidationError("Only .xlsx or .xls files are allowed.")
        if not course_code:
            raise forms.ValidationError("Course code is required")
    
        return cleaned_data                                                                              
   ''' 


class UploadForm(forms.Form):
    file = forms.FileField(label='Select an Excel file')
    year_of_file = forms.ModelChoiceField(
        queryset=File_Description.objects.values_list('year_of_file', flat=True).distinct(),
        empty_label="Select Year of the File"
    )
    course_code = forms.ModelChoiceField(
        queryset=File_Description.objects.values_list('course__course_code', flat=True).distinct(),
        empty_label="Select Course Code"
    )

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        course_code = cleaned_data.get('course_code')
        year_of_file = cleaned_data.get('year_of_file')

        if not file:
            raise forms.ValidationError("Excel file is required.")
        
        if not file.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError("Only .xlsx or .xls files are allowed.")

        if not course_code:
            raise forms.ValidationError("Course code is required.")
        
        if not year_of_file:
            raise forms.ValidationError("Year of the file is required.")
    
        return cleaned_data
>>>>>>> error
