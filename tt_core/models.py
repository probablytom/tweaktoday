from django.db import models
from mimetypes import guess_type
from django.conf import settings
import datetime


# Create your models here.
class TaskSuggestion(models.Model):
    task_text = models.CharField(max_length=200)
    task_explainer = models.CharField(max_length=1000, blank=True)
    task_voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    @property
    def votes(self):
        return len(list(self.task_voters.all()))


class Mission(models.Model):
    task_text = models.CharField(max_length=200)
    task_explainer = models.CharField(max_length=1000, blank=True)
    task_voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    date_assigned = models.DateField(default=datetime.date.today)

    @property
    def votes(self):
        return len(list(self.task_voters.all()))

    def __str__(self):
        return self.task_text


class Submission(models.Model):
    tweak_submitted_to = models.ForeignKey(Mission, on_delete=models.CASCADE, blank=False)
    tweak_url = models.URLField(max_length=1000, blank=True)
    extra_content = models.ImageField(blank=True, upload_to="photos/%Y/%m/%d")
    submission_explainer = models.CharField(max_length=2000, default="")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submission_datetime = models.DateTimeField(auto_now_add=True)
    mime = models.CharField(max_length=30, default="photo/jpeg")
    is_video = models.BooleanField(default=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            self.mime = guess_type(self.extra_content.url)[0]
            self.is_video = self.mime.split('/')[0] == 'video'
        except:
            pass
        super().save(*args, **kwargs)


class Comment(models.Model):
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
