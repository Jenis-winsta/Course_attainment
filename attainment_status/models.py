from django.db import models

# Create your models here.
class Data(models.Model):    
    name = models.CharField(max_length=100)
    cia_marks = models.IntegerField()
    ese_marks = models.IntegerField()
    total_marks = models.IntegerField()
    
    def __str__(self):
        return f'{self.name}, {self.total_marks}'  