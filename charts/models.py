# models.py
from django.db import models
from techapp.models import *


class File_Description(models.Model):
    year_of_file = models.CharField(max_length=20)            
    course = models.ForeignKey(Course, on_delete=models.CASCADE)     # techapp course models

    def __str__(self):
        return f"{self.year_of_file} --> {self.course.course_code}"


class Student(models.Model):
    name = models.CharField(max_length=250) 
    cia_marks = models.IntegerField()
    semester_marks = models.IntegerField()
    total_marks = models.IntegerField()  
    file_desc = models.ForeignKey(File_Description, on_delete=models.CASCADE)
    
    

    # list_display = ('name', 'cia_marks', 'semester_marks', 'total_marks', 'file_desc',)
        
    # def __str__(self):
    #     return f'{self.list_display}' 
    
    
    

    