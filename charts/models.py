# models.py
from django.db import models
from techapp.models import *




class PassoutYear(models.Model):
    year = models.IntegerField(unique=True)  # Example: 2022, 2023, etc.

    def __str__(self):
        return str(self.year)
    


class AttainmentPercentage(models.Model):
    passout_year = models.ForeignKey(PassoutYear, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attainment_percentage = models.FloatField()

    def __str__(self):
        return f"{self.course} ({self.passout_year}): {self.attainment_percentage}%"

class File_Description(models.Model):
    passout_year = models.ForeignKey(PassoutYear, on_delete=models.CASCADE)            
    course = models.ForeignKey(Course, on_delete=models.CASCADE)     # techapp course models

    def __str__(self):
        return f"{self.course.course_code} (Passout: {self.passout_year})"
    



class Student(models.Model):
    name = models.CharField(max_length=250) 
    cia_marks = models.IntegerField()
    semester_marks = models.IntegerField()
    total_marks = models.IntegerField()  
    file_desc = models.ForeignKey(File_Description, on_delete=models.CASCADE)
    
    


    
    
    

    