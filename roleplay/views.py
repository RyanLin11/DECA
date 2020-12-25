from django.shortcuts import render, redirect
from .models import Case, Submission
from .forms import SubmissionForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'roleplay/index.html', {'cases': Case.objects.all()})

@login_required(login_url='accounts:login')
def case(request, pk):
    form = SubmissionForm()
    if request.method == 'POST':
        sub = Submission(student=request.user, case=Case.objects.get(pk=pk))
        form = SubmissionForm(request.POST, request.FILES, instance=sub)
        if form.is_valid():
            form.save()
        return redirect('roleplay')
    return render(request, 'roleplay/case.html', {'case':Case.objects.get(pk=pk), 'form':form, 'submissions':Submission.objects.filter(student=request.user).order_by('-date')})

@login_required(login_url='accounts:login')
def feedback(request, pk):
    return render(request, 'roleplay/feedback.html', {'submission': Submission.objects.get(pk=pk)})