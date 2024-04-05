from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import *


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    
    list_display = ('name', 'cia_marks', 'semester_marks', 'total_marks',)
    


admin.site.register(File_Description)