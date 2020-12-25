from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "leaderboard/index.html", {'Users':users})