import os
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from main.models import Summary
from main.validators import validate_youtube_url, validate_youtube_duration, validate_audio_duration
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

        self._validate_link_or_file(youtube_link, audio_file)

        time_left, error_message = self._get_user_time()

        if youtube_link:
            self._validate_youtube(youtube_link, time_left, error_message)

        if audio_file:
            self._validate_audio_file(audio_file, time_left, error_message)
        return cleaned_data

    def _validate_link_or_file(self, youtube_link, audio_file):
        if not youtube_link and not audio_file or youtube_link and audio_file:
            raise forms.ValidationError('Введите либо ссылку на ютуб, либо загрузите файл')

    def _get_user_time(self):
        if self.user and self.user.is_authenticated:
            time_left = self.user.time_left
            error_message = f"Видео превышает по длине Ваше доступное время ({time_left} минута)"
        else:
            time_left = settings.ALLOWED_TIME_UNAUTH_USER
            error_message = f"Неавторизованные пользователи могут загружать видео продолжительностью " \
                            f"не более {time_left} минут"
        return time_left, error_message

    def _validate_youtube(self, youtube_link, time_left, error_message):
        validate_youtube_url(youtube_link)
        if not validate_youtube_duration(youtube_link, time_left):
            raise forms.ValidationError(error_message)

    def _validate_audio_file(self, audio_file, time_left, error_message):
        extension = os.path.splitext(audio_file.name)[1][1:].lower()
        if extension not in settings.SUPPORTED_EXTENSIONS:
            raise forms.ValidationError("Неподдерживаемое расширение файла")
        if not validate_audio_duration(audio_file, time_left):
            raise forms.ValidationError(error_message)

