from django.shortcuts import render, redirect
from .models import Exam
from .models import Question
from .models import Choice
from .models import UserExam
from .models import UserAnswer
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    context = {}
    if request.user.profile.event is not None:
        exams = Exam.objects.filter(exam_cluster=request.user.profile.event.cluster)
    else:
        exams = Exam.objects.all()
    exams_dict = {}
    for exam in exams:
        exams_dict[exam] = UserExam.objects.filter(exam=exam, user=request.user).order_by('-date').first()
    context['exams'] = exams_dict
    return render(request, 'quiz/index.html', context)

@login_required(login_url='accounts:login')
def exam(request, num):
    if request.method == 'POST':
        exam = Exam.objects.get(exam_number=num)
        questions = Question.objects.filter(exam=exam)
        user_exam = UserExam.objects.filter(exam=exam, user=request.user).order_by('-date').first()
        answers = UserAnswer.objects.filter(user_exam=user_exam)
        score = 0
        num_answered = 0
        for question in questions:
            if str(question.pk) in request.POST:
                try:
                    answer = answers.get(question=question)
                    answer.choice = Choice.objects.get(pk=int(request.POST[str(question.pk)]))
                except UserAnswer.DoesNotExist:
                    answer = UserAnswer(user_exam=user_exam,question=question, choice=Choice.objects.get(pk=int(request.POST[str(question.pk)])))
                finally:
                    answer.save()
                if answer.choice.is_correct:
                    score += 1
                num_answered += 1
        if num_answered == questions.count():
            user_exam.is_finished = True
            user_exam.score = score
            user_exam.date = timezone.now()
            user_exam.save()
            return redirect('quiz:results', num=exam.exam_number)
        return redirect('quiz:quiz')
    else:
        context = {}
        context['Exam'] = Exam.objects.get(exam_number=num)
        #get the userExam object that is linked with user's answers
        userExam = UserExam.objects.filter(exam=context['Exam'], user=request.user).order_by('-date').first()
        if userExam is None or userExam.is_finished:
            userExam = UserExam.objects.create(exam=context['Exam'], user=request.user)
        #put all the filled answers into a dictionary
        filled = {}
        answers = UserAnswer.objects.filter(user_exam=userExam)
        for question in Question.objects.filter(exam=context['Exam']):
            try:
                filled[question] = answers.get(question=question).choice
            except UserAnswer.DoesNotExist:
                filled[question] = None
        context['filled'] = filled
        #render exam template
        return render(request, 'quiz/exam.html', context)

@login_required(login_url='accounts:login')
def results(request, num):
    user_exam = UserExam.objects.filter(exam__exam_number=num, user=request.user).order_by('-date').first()
    all_answers = UserAnswer.objects.filter(user_exam=user_exam)
    correct_answers = all_answers.filter(choice__is_correct=True)
    incorrect_answers = all_answers.filter(choice__is_correct=False)
    return render(request, 'quiz/result.html', {'correct':correct_answers, 'incorrect':incorrect_answers})