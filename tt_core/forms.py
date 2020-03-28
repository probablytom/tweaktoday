from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class SubmissionForm(forms.Form):
    submission_url = forms.URLField(max_length=1000, required=False)
    submission_photo_or_video = forms.FileField(required=False)
    explanatory_text = forms.CharField(widget=forms.Textarea, max_length=2000)


class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea, max_length=2000)