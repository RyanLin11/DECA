from django.shortcuts import render
from .models import Case
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'roleplay/index.html', {'cases': Case.objects.all()})

@login_required(login_url='accounts:login')
def case(request, pk):
    return render(request, 'roleplay/case.html', {'case':Case.objects.get(pk=pk)})