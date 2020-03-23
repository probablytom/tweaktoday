from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


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

@login_required
def voteon(request, suggestion_id):
    '''
    Allows a logged in user to vote on a suggestion
    :param request: the django http request
    :param suggestion_id: The id of the suggestion being voted on
    :return: redirect to vote_recieved
    '''
    suggestion = TaskSuggestion.objects.get(pk=suggestion_id)
    # Get logged in user
    user = request.user
    suggestion.task_voters.add(user)
    # suggestion.save()
    # Add user to suggestion many-to-many
    # Render an appropriate template and return it
    return redirect('tt_core:suggestions')

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
    suggestion = TaskSuggestion.objects.get(pk=suggestion_id)
    user = request.user
    suggestion.task_voters.remove(user)
    return redirect('tt_core:suggestions')

def suggestions(request):
    '''
    Lists all of the current suggestions
    :param request: The django http request
    :return: A rendered suggestions template
    '''
    suggs = list(TaskSuggestion.objects.all())
    suggs = sorted(suggs, key=lambda s: -s.votes)
    return render(request, 'tt_core/suggestions.html', {'suggs': suggs})

def post_submission(request):
    '''
    Adds a new submission to the list
    :param request: The django http request
    :return: A redirect to submission_recieved
    '''
    return HttpResponse('post_submission')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')  # TODO: change '/' to tt_core:index
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            print(username)
            print(password)
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            error_message = 'Something went wrong registering the new user! Try again...'
            print(form.errors)
            return render(request, 'tt_core/register.html', {'form': form, 'error': error_message})
    else:
        form = UserCreationForm()
        return render(request, 'tt_core/register.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return index(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(username)
        print(password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'tt_core/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'tt_core/login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/')

@login_required
def suggest_new_task(request):
    if request.method == 'POST':
        try:
            # New submission given!
            challenge_text = request.POST['suggestion_text']
            challenge_explainer = request.POST['explainer_text']
            if challenge_text == "":
                return render(request, 'tt_core/new_suggestion.html', {'error': "You can't submit a challenge without a challenge title!"})
            sug = TaskSuggestion(task_text=challenge_text,
                                 task_explainer=challenge_explainer)
            sug.save()
            return redirect('tt_core:suggestions')
        except Exception as e:
            print(e)
            return render(request, 'tt_core/new_suggestion.html', {'error': 'We encountered an error processing your suggestion! Could you try again?'})
    else:
        return render(request, 'tt_core/new_suggestion.html')
