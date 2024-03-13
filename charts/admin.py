# admin.py
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('file_name', 'name', 'cia_marks', 'sem_marks', 'total_marks')
    
admin.site.register(File_Description)