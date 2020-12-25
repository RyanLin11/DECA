from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Cluster(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    team = models.BooleanField(default=False)  

    def __str__(self):
        return self.code

class Case(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    REGIONALS = 'R'
    PROVINCIALS = 'P'
    ICDC = 'I'
    LEVELS = [
        (REGIONALS, 'Regionals'),
        (PROVINCIALS, 'Provincials'),
        (ICDC, 'ICDC'),
    ]
    level = models.CharField(max_length=1, choices=LEVELS)

    def __str__(self):
        return self.title

class PI(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class CaseQuestion(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Submission(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    audio_file = models.FileField(upload_to="case/audio/")
    
    def __str__(self):
        return self.case.title+" ("+self.student.username+")"