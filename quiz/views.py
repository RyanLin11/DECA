from django.shortcuts import render, redirect
from .models import Exam
from .models import Question
from .models import Choice
from .models import UserExam
from .models import UserAnswer
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    exams = {'Exams':Exam.objects.all()}
    return render(request, 'quiz/index.html', exams)

@login_required(login_url='accounts:login')
def exam(request, num):
    context = {'Questions': Question.objects.filter(exam__exam_number=num), 'Exam': Exam.objects.get(exam_number=num)}
    try:
        context['Answers'] = UserAnswer.objects.filter(user_exam=UserExam.objects.get(exam__exam_number=num))
    except UserExam.DoesNotExist:
        pass
    try:
        userExam = UserExam.objects.get(exam__exam_number=num)
        if userExam.is_finished:
            userExam.delete()
            userExam = UserExam.objects.create(exam=context['Exam'], user=request.user)
        context['userExam'] = userExam
    except UserExam.DoesNotExist:
        userExam = UserExam.objects.create(exam=context['Exam'], user=request.user)
        context['userExam'] = userExam
    return render(request, 'quiz/exam.html', context)

@login_required(login_url='accounts:login')
def grade(request, num):
    if request.method == 'POST':
        questions = Question.objects.filter(exam__exam_number=num)
        answered_questions = []
        user_exam = UserExam.objects.get(exam__exam_number=num)
        for question in questions:
            if str(question.pk) in request.POST:
                try:
                    answer = UserAnswer.objects.get(question=question)
                    answer.user_exam = user_exam
                    answer.question = question
                    answer.choice = Choice.objects.get(pk=int(request.POST[str(question.pk)]))
                    answer.save()
                    answered_questions.append(answer)
                except UserAnswer.DoesNotExist:
                    answer = UserAnswer(user_exam=user_exam,question=question, choice=Choice.objects.get(pk=int(request.POST[str(question.pk)])))
                    answer.save()
                    answered_questions.append(answer)
        if len(answered_questions) == len(questions):
            score = 0
            for answer in answered_questions:
                if answer.choice.is_correct:
                    score+=1
            user_exam.is_finished = True
            user_exam.score = score
            user_exam.save()
        return redirect('quiz:quiz')
    return render(request, 'quiz/index.html')
    
                
            