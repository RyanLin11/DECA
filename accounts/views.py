from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm, ChangeUserForm, CreateUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from roleplay.models import Submission
from quiz.models import UserExam, Exam
from datetime import date
import json
from django.db import models

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('quiz:quiz')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:login')
        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('quiz:quiz')
    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quiz:quiz')
        context = {'form':form}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('accounts:login')

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
    #calculate statistics
    finished_exams = finished_exams_sorted.values("exam").distinct().count()
    inprogress_exams = exams.values("exam").distinct().count() - finished_exams
    new_exams = Exam.objects.all().count() - finished_exams - inprogress_exams
    return render(request, 'accounts/index.html', {'submissions': Submission.objects.filter(marked=True),'date':date.today(), 'profile':request.user.profile, 'titles':json.dumps(titles), 'scores':json.dumps(scores), 'finished_exams':json.dumps(finished_exams), 'inprogress_exams':json.dumps(inprogress_exams), 'new_exams':json.dumps(inprogress_exams)})
