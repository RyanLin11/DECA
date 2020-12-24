from django.contrib import admin
from .models import Question
from .models import Exam
from .models import Choice
from .models import UserExam
from .models import UserAnswer

# Register your models here.
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserExam)
admin.site.register(UserAnswer)