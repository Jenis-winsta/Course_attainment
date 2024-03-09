# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    cia_marks = models.IntegerField()
    sem_marks = models.IntegerField()
    total_marks = models.IntegerField()

