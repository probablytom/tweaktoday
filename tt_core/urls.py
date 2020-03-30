from . import views
from django.urls import path, re_path

app_name = 'tt_core'

urlpatterns = [
    path('', views.index, name='index'),
    path('voteon/<int:suggestion_id>', views.voteon, name='submit_vote'),
    path('remove_vote/<int:suggestion_id>', views.remove_vote, name='remove_vote'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('register', views.register_user, name='register_new_user'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='signout'),
    path('archive', views.view_archive, name='archive'),
    path('mission/<int:mission_id>', views.view_past_mission, name='view_mission'),
    path('submit_mission/<int:mission_id>', views.post_submission, name='post_submission'),
    path('view_comments/<int:submission_id>', views.view_comments, name='view_comments'),
    path('profile/<str:username>', views.view_profile, name='profile'),
    re_path('photos/.*', views.stream_video, name='stream_video'),
    path('contribute', views.view_contribute_page, name='contribute'),
    path('delete_submission/<int:submission_id>', views.delete_submission, name='delete_submission'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
]