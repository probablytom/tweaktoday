from django.db import models
from django.conf import settings


# Create your models here.
class TaskSuggestion(models.Model):
    task_text = models.CharField(max_length=200)
    task_explainer = models.CharField(max_length=1000, blank=True)
    task_voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    @property
    def votes(self):
        return len(list(self.task_voters.all()))


class Tweak(TaskSuggestion):
    pass


class Submission(models.Model):
    tweak_submitted_to = models.ForeignKey(Tweak, on_delete=models.CASCADE)
    tweak_url = models.URLField(max_length=1000, default="", blank=True)
    submission_explainer = models.CharField(max_length=2000, default="")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
