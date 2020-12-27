from django.contrib import admin
from .models import Question, Exam, Choice, UserExam, UserAnswer, InstructionalArea

class ChoiceInline(admin.TabularInline):
    model = Choice
    max_num=4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class UserExamInline(admin.TabularInline):
    model = UserExam
    extra=0

class ExamAdmin(admin.ModelAdmin):
    inlines = [UserExamInline]
    list_display = ('exam_number','exam_cluster',)

# Register your models here.
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(InstructionalArea)