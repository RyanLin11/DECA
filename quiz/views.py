from django.shortcuts import render, redirect
from .models import Exam
from .models import Question
from .models import Choice
from .models import UserExam
from .models import UserAnswer
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def index(request):
    """
    Displays a list of exams tailored to a student's competitive event.
    """
    context = {}
    #get the list of exams in order of recency
    exams = Exam.objects.all()
    #only get exams relevant to the user's event if it is specified
    if request.user.profile.event is not None:
        exams = exams.filter(exam_cluster=request.user.profile.event.cluster)
    #collect exam information to display
    exams_dict = {}
    for exam in exams:
        #get all submissions this user made to this exam
        submitted_exams = UserExam.objects.filter(exam=exam, user=request.user)
        #only direct students to the most recent exam
        most_recent_exam = submitted_exams.order_by('-date').first()
        is_finished = most_recent_exam.is_finished
        is_started = most_recent_exam is None
        #determine the highest score for this exam
        high_score = 0
        for subexam in submitted_exams:
            high_score = max(high_score, subexam.score)
        exams_dict[exam] = {'is_finished': is_finished, 'is_started':is_started, 'high_score':high_score, 'most_recent_exam': most_recent_exam}
    context['exams'] = exams_dict
    #render the template
    return render(request, 'quiz/index.html', context)

@login_required(login_url='accounts:login')
def exam(request, num):
    """
    Displays all the questions of an exam
    """
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
    """
    Displays the results from a user's submitted exam
    """
    user_exam = UserExam.objects.filter(exam__exam_number=num, user=request.user).order_by('-date').first()
    all_answers = UserAnswer.objects.filter(user_exam=user_exam)
    correct_answers = all_answers.filter(choice__is_correct=True)
    incorrect_answers = all_answers.filter(choice__is_correct=False)
    return render(request, 'quiz/result.html', {'correct':correct_answers, 'incorrect':incorrect_answers})