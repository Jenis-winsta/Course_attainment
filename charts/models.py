# models.py
from django.db import models
from techapp.models import *

class Student(models.Model):
    name = models.CharField(max_length=100)
    cia_marks = models.IntegerField()
    sem_marks = models.IntegerField()
    total_marks = models.IntegerField()  
    file_name = models.CharField(max_length=100)

    list_display = ('name', 'cia_marks', 'sem_marks', 'total_marks', 'file_name',)
        
    def __str__(self):
        return f'{self.list_display}' 
    
    
class File_Description(models.Model):
    year = models.IntegerField()    
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    

    