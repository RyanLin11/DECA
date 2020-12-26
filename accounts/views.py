from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile

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
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz')
    else:
        if not hasattr(request.user, 'profile'):
            profile = Profile(user=request.user)
            profile.save()
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', context = {'form':form})
