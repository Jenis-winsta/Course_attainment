# models.py
from django.db import models
from techapp.models import *


class File_Description(models.Model):
    year = models.CharField(max_length=10)    
    sheet_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.sheet_name:
            return f"{self.year} - {self.sheet_name}"
        else:
            return str(self.year)

class Student(models.Model):
    name = models.CharField(max_length=250)
    cia_marks = models.IntegerField()
    semester_marks = models.IntegerField()
    total_marks = models.IntegerField()  
    file_desc = models.ForeignKey(File_Description, on_delete=models.CASCADE)
    
    

    # list_display = ('name', 'cia_marks', 'semester_marks', 'total_marks', 'file_desc',)
        
    # def __str__(self):
    #     return f'{self.list_display}' 
    
    
    

    