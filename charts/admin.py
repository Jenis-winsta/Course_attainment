# admin.py
from django.contrib import admin
from .models import Student
from import_export.admin import ImportExportModelAdmin


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'cia_marks', 'sem_marks', 'total_marks')