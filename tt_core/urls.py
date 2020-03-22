from . import views
from django.urls import path

app_name = 'tt_core'

urlpatterns = [
    path('', views.index, name='index'),
    path('voteon/<int:suggestion_id>', views.voteon, name='submit_vote'),
    path('remove_vote/<int:suggestion_id>', views.remove_vote, name='remove_vote'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('register', views.register_user, name='register_new_user'),
    path('make_suggestion', views.suggest_new_task, name='suggest_new_task')
]