from .models import Submission

def add_submissions(request):
    return {'marked_submissions': Submission.objects.filter(marked=True)}