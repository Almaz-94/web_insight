from django.forms import ModelForm

from main.models import Summary
from main.services import get_user_time
from main.validators import \
    validate_link_or_file, \
    validate_youtube, \
    validate_audio_file
from users.forms import StyleFormMixin


class SummaryForm(StyleFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Summary
        fields = ('youtube_link', 'audio_file', 'script', 'prompt', )

    def clean(self):
        cleaned_data = super().clean()
        youtube_link = cleaned_data.get('youtube_link')
        audio_file = cleaned_data.get('audio_file')

        validate_link_or_file(youtube_link, audio_file)

        time_left, error_message = get_user_time(self.user)

        if youtube_link:
            validate_youtube(youtube_link, time_left, error_message)

        if audio_file:
            validate_audio_file(audio_file, time_left, error_message)

        return cleaned_data

