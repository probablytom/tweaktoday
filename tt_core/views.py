from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(_request):
    '''
    Shows today's tweak and the relevant submissions for it
    :param _request: The django http request
    :return: Rendered index template containing today's tweak and its submissions
    '''
    return HttpResponse('You are at the index of TweakToday.')

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
    return HttpResponse('suggetsions')

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
