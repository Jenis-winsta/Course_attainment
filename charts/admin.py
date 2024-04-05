from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import *


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    
<<<<<<< HEAD
    list_display = ( 'file_desc', 'name', 'cia_marks', 'semester_marks', 'total_marks',)
=======
    list_display = ('name', 'cia_marks', 'semester_marks', 'total_marks',)
>>>>>>> error
    


admin.site.register(File_Description)
