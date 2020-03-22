from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    '''
    Shows today's tweak and the relevant submissions for it
    :param _request: The django http request
    :return: Rendered index template containing today's tweak and its submissions
    '''
    challenge = Tweak.objects.all()[0]
    submissions = list(challenge.submission_set.all().iterator())
    return render(request, 'tt_core/index.html', context={'challenge': challenge, 'submissions':submissions})

def voteon(request, suggestion_id):
    '''
    Allows a logged in user to vote on a suggestion
    :param request: the django http request
    :param suggestion_id: The id of the suggestion being voted on
    :return: redirect to vote_recieved
    '''
    return HttpResponse('voteon')

def vote_recieved(request):
    '''
    Tells a user their vote was recieved.
    :param request: the django http request
    :return: A rendered vote_recieved template
    '''
    return HttpResponse('vote recieved')

def submission_recieved(request):
    '''
    Tells a user their submission was recieved.
    :param request: the django http request
    :return: A rendered submission_recieved template
    '''
    return HttpResponse('submission recieved')

def remove_vote(request, suggestion_id):
    '''
    Removes a vote made by a user
    :param request: the django http request
    :param suggestion_id: the suggestion for which the vote is being removed
    :return: A rendered vote_removed template
    '''
    return HttpResponse('remove vote')

def suggestions(request):
    '''
    Lists all of the current suggestions
    :param request: The django http request
    :return: A rendered suggestions template
    '''
    suggs = TaskSuggestion.objects.all()
    return render(request, 'tt_core/suggestions.html', {'suggs': suggs})

def post_submission(request):
    '''
    Adds a new submission to the list
    :param request: The django http request
    :return: A redirect to submission_recieved
    '''
    return HttpResponse('post_submission')

def register_user(request):
    '''
    Register a new user
    :param request:
    :return:
    '''
    raise NotImplemented()

def suggest_new_task(request):
    return HttpResponse('in suggest new task')
