from django import forms
from django.forms import ModelForm
import re

from main.models import Summary
from main.services import validate_youtube_url
from users.forms import StyleFormMixin


class SummaryForm(StyleFormMixin, ModelForm):
    link = forms.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Summary
        fields = ('link', 'script', 'prompt', )


