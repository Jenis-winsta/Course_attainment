from django import forms
from .models import Student

class StudentData(forms.Form):
	class meta:
		model = Student
		fields = '__all__'