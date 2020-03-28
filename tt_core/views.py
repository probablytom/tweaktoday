from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SubmissionForm, CommentForm
from .scheduling import *
import datetime

# === from https://stackoverflow.com/questions/33208849/python-django-streaming-video-mp4-file-using-httpresponse#41289535
import os
import re
import mimetypes
from wsgiref.util import FileWrapper

from django.http.response import StreamingHttpResponse


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream_video(request):
    path = request.path[1:]
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
 # === end from https://stackoverflow.com/questions/33208849/python-django-streaming-video-mp4-file-using-httpresponse#41289535

# Create your views here.
def index(request):
    '''
    Shows today's tweak and the relevant submissions for it
    :param _request: The django http request
    :return: Rendered index template containing today's tweak and its submissions
    '''
    try:
        challenge = Mission.objects.order_by('-date_assigned')[0]
    except Exception as e:
        return render(request, 'tt_core/index.html', context={'challenge': None, 'submissions': None})

    submissions = list() if challenge.submission_set.all().count() is 0 \
                         else list(challenge.submission_set.order_by('-submission_datetime').iterator())

    return render(request, 'tt_core/index.html', context={'challenge': challenge,
                                                          'submissions':submissions,
                                                          'submission_form': SubmissionForm()})


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


def suggestions(request, error="", submission_message=""):
    '''
    Lists all of the current suggestions
    :param request: The django http request
    :return: A rendered suggestions template
    '''
    def suggs():
        suggs = list(TaskSuggestion.objects.all())
        suggs = sorted(suggs, key=lambda s: -s.votes)
        return suggs
    if request.method == 'POST':
        try:
            # New submission given!
            challenge_text = request.POST['suggestion_text']
            challenge_explainer = request.POST['explainer_text']
            if challenge_text == "":
                return render(request, 'tt_core/suggestions.html', {'error': "You can't submit a challenge without a challenge title!",
                                                                    'suggs': suggs()})
            sug = TaskSuggestion(task_text=challenge_text,
                                 task_explainer=challenge_explainer)
            sug.save()
            return render(request, 'tt_core/suggestions.html', {'suggs': suggs()})
        except Exception as e:
            print(e)
            return render(request, 'tt_core/suggestions.html', {'error': 'We encountered an error processing your suggestion! Could you try again?',
                                                                'suggs': suggs()})
    else:
        return render(request, 'tt_core/suggestions.html', {'suggs': suggs()})

@login_required
def suggest_new_task(request):
    pass


@login_required
def post_submission(request, mission_id):
    '''
    Adds a new submission to the list
    :param request: The django http request
    :param mission_id: The pk of the mission being submitted to
    :return: A redirect to submission_recieved
    '''
    mission = Mission.objects.get(pk=mission_id)
    try:
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            explaination = form.cleaned_data.get('explanatory_text')
            url = form.cleaned_data.get('submission_url')
            img = form.cleaned_data.get('submission_photo_or_video')
            newsub = Submission(submission_explainer=explaination,
                                tweak_url=url,
                                extra_content=img,
                                submitted_by=request.user,
                                tweak_submitted_to=mission)
            newsub.save()
            return render(request, 'tt_core/index.html', {'challenge': mission,
                                                          'submissions': mission.submission_set.order_by('-submission_datetime'),
                                                          'submission_form': SubmissionForm(),
                                                          'submission_message': 'Submission successfully posted!'})
        else:
            print('invalid!')
            return render(request, 'tt_core/index.html', {'challenge': mission,
                                                          'submissions': mission.submission_set.order_by('-submission_datetime'),
                                                          'submission_form': SubmissionForm(),
                                                          'submission_message': "Couldn't accept your submission! Maybe we found an invalid URL, or there was an issue with a photo."})
        # if request.FILES['submission_photo_or_video']
    except:
        print('error')
        return render(request, 'tt_core/index.html', {'challenge': mission,
                                                      'submissions': mission.submission_set.order_by(
                                                          '-submission_datetime'),
                                                      'submission_form': SubmissionForm(),
                                                      'submission_message': 'Submission successfully posted!'})


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
def post_comment(request):
    pass


def view_past_mission(request, mission_id):
    try:
        mission = Mission.objects.get(pk=mission_id)
        submissions = list() if mission.submission_set.order_by('-submission_datetime').count() is 0 \
            else list(mission.submission_set.all().iterator())
        return render(request, 'tt_core/mission.html', {'challenge': mission,
                                                        'submissions': submissions})
    except:
        return render(request, 'tt_core/mission.html', {'challenge': None,
                                                        'submissions': None})



def view_archive(request):
    missions = Mission.objects.filter(date_assigned__lt=datetime.date.today())
    return render(request, 'tt_core/archive.html', {'past_missions': missions})

def view_comments(request, submission_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            sub = Submission.objects.get(pk=submission_id)
            comments = sub.comment_set.order_by('-timestamp')
            return render(request, 'tt_core/view_comments.html', {'sub': sub,
                                                                  'comments': comments,
                                                                  'form': CommentForm(),
                                                                  'error': 'You have to be logged in to leave comments!'})
        form = CommentForm(request.POST)
        if form.is_valid():
            sub = Submission.objects.get(pk=submission_id)
            new_comment = Comment(comment_text=form.cleaned_data.get('comment_text'),
                                  commenter=request.user,
                                  submission=sub)
            new_comment.save()
            comments = sub.comment_set.order_by('-timestamp')
            return render(request, 'tt_core/view_comments.html', {'sub': sub,
                                                                  'comments': comments,
                                                                  'form': CommentForm()})
        else:
            sub = Submission.objects.get(pk=submission_id)
            comments = sub.comment_set.order_by('-timestamp')
            return render(request, 'tt_core/view_comments.html', {'sub': sub,
                                                                  'comments': comments,
                                                                  'form': CommentForm(),
                                                                  'error': 'There was an error with your form in adding your comment! Not sure what it could be. Sorry…'})
    else:
        sub = Submission.objects.get(pk=submission_id)
        comments = sub.comment_set.order_by('-timestamp')
        return render(request, 'tt_core/view_comments.html', {'sub': sub,
                                                              'comments': comments,
                                                              'form': CommentForm()})

def view_profile(request, username):
    user = User.objects.get(username=username)
    posts = []
    for submission in Submission.objects.filter(submitted_by=user).order_by('-submission_datetime'):
        posts.append((submission.tweak_submitted_to, submission))
    # posts = {subs.tweak_submitted_to: subs for subs in Submission.objects.filter(submitted_by=user)}
    return render(request, 'tt_core/profile.html', {'posts': posts})
