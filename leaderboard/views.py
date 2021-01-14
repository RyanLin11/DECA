from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from roleplay.models import Submission
from quiz.models import UserExam


# Create your views here.
@login_required(login_url='accounts:login')
def index(request):
    User = get_user_model()
    users = User.objects.all()
    #determine points
    #get highest score per exam
    point = {}
    for user in users:
        hi_scores = {}
        for user_exam in UserExam.objects.filter(user=user, is_finished=True):
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
        subs = set()
        for submission in Submission.objects.filter(student=request.user, marked=True):
            subs.add(submission.case)
        points += len(subs) * 100
        point[user] = points
    return render(request, "leaderboard/index.html", {'users':users, 'points':point})