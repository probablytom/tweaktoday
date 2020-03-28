from django.contrib import admin
from .models import Mission, TaskSuggestion, Submission, Comment

# Register your models here.
admin.site.register(Mission)
admin.site.register(TaskSuggestion)
admin.site.register(Submission)
admin.site.register(Comment)
