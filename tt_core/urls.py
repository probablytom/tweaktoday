from . import views
from django.urls import path

app_name = 'tt_core'

urlpatterns = [
    path('', views.index, name='index'),
    path('voteon/<int:suggestion_id>', views.voteon, name='submit_vote'),
    path('remove_vote/<int:suggestion_id>', views.remove_vote, name='remove_vote'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('register', views.register_user, name='register_new_user'),
    # path('make_suggestion', views.suggest_new_task, name='suggest_new_task'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='signout'),
    path('archive', views.view_archive, name='archive'),
    path('mission/<int:mission_id>', views.view_past_mission, name='view_mission'),
    path('submit_mission/<int:mission_id>', views.post_submission, name='post_submission'),
    path('view_comments/<int:submission_id>', views.view_comments, name='view_comments'),
    path('profile/<str:username>', views.view_profile, name='profile'),
]