from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm, ChangeUserForm, CreateUserForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from roleplay.models import Submission
from quiz.models import UserExam, Exam, InstructionalArea
import json
from django.db import models
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('quiz:quiz')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            print('post lol')
            if form.is_valid():
                form.save()
                return redirect('accounts:login')
            print('not success')
        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('quiz:quiz')
    else:
        form = LoginForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:index')
            print('failed')
        context = {'form':form}
        return render(request, 'accounts/login.html', context)

@login_required(login_url='accounts:login')
def logoutUser(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            return redirect('quiz:quiz')
    else:
        if not hasattr(request.user, 'profile'):
            profile = Profile(user=request.user)
            profile.save()
        user_form = ChangeUserForm(instance=request.user)
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', context = {'user_form':user_form,'form':form})

@login_required(login_url='accounts:login')
def index(request):
    exams = UserExam.objects.filter(user=request.user)
    finished_exams_sorted = exams.filter(is_finished=True).order_by('date')
    titles = []
    scores = []
    for user_exam in finished_exams_sorted:
        titles.append("Exam "+str(user_exam.exam.exam_number))
        scores.append(user_exam.score)
    titles_json = json.dumps(titles)
    scores_json = json.dumps(scores)
    #calculate number of exams completed
    distinct_started = exams.values("exam").distinct().count()
    finished_exams = finished_exams_sorted.values("exam").distinct().count()
    inprogress_exams = distinct_started - finished_exams
    new_exams = Exam.objects.all().count() - distinct_started
    #calculate percentage correct
    ia_correct = {}
    instructional_areas = InstructionalArea.objects.all()
    for ia in instructional_areas:
        correct = 0
        total = 0
        for question in ia.question_set.all():
            for answer in question.useranswer_set.filter(user_exam__user=request.user):
                if answer.choice.is_correct:
                    correct+=1
                total+=1
        if total > 0:
            ia_correct[ia.title] = int(correct/total * 100)
    #determine points
    #get highest score per exam
    hi_scores = {}
    for user_exam in UserExam.objects.filter(user=request.user, is_finished=True):
        exam = user_exam.exam
        if exam in hi_scores:
            hi_scores[exam] = max(user_exam.score, hi_scores[exam])
        else:
            hi_scores[exam] = user_exam.score
    #sum up highest exam scores
    points = 0
    for score in hi_scores.values():
        points += score
    #get number of unique roleplay submissions
    subs = {}
    for submission in Submission.objects.filter(student=request.user, marked=True):
        subs.add(submission.case)
    points += len(subs) * 100
    return render(request, 'accounts/index.html', {'submissions': Submission.objects.filter(marked=True),'date':date.today(), 'profile':request.user.profile, 'titles':json.dumps(titles), 'scores':json.dumps(scores), 'finished_exams':json.dumps(finished_exams), 'inprogress_exams':json.dumps(inprogress_exams), 'new_exams':json.dumps(new_exams), 'ia_correct':ia_correct, 'points':points})
