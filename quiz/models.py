from django.db import models
from django.contrib.auth.models import User
from roleplay.models import Cluster
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Exam(models.Model):
    exam_number = models.IntegerField()
    exam_cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.exam_number)

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    question_explanation = models.TextField(default="N/A")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=250)
    is_correct = models.BooleanField()
    def __str__(self):
        return self.choice_text

class UserExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username + " "+ str(self.exam.exam_number)

class UserAnswer(models.Model):
    user_exam = models.ForeignKey(UserExam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def __str__(self):
        return self.choice.choice_text