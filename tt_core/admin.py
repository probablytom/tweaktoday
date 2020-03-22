from django.contrib import admin
from .models import Tweak, TaskSuggestion, Submission

# Register your models here.
admin.site.register(Tweak)
admin.site.register(TaskSuggestion)
admin.site.register(Submission)
