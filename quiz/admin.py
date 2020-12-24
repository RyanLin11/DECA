from django.contrib import admin
from .models import Question, Exam, Choice, UserExam, UserAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    max_num=4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

# Register your models here.
admin.site.register(Exam)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserExam)
admin.site.register(UserAnswer)