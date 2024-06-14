import os
import re

from django.conf import settings
from django.core.exceptions import ValidationError

from main.services import get_youtube_video_duration, get_audio_duration


def validate_link_or_file(youtube_link, audio_file):
    if not youtube_link and not audio_file or youtube_link and audio_file:
        raise ValidationError('Введите либо ссылку на ютуб, либо загрузите файл')


def validate_youtube(youtube_link, time_left, error_message):
    validate_youtube_url(youtube_link)
    if get_youtube_video_duration(youtube_link) > time_left:
        raise ValidationError(error_message)


def validate_audio_file(audio_file, time_left, error_message):
    extension = os.path.splitext(audio_file.name)[1][1:].lower()
    if extension not in settings.SUPPORTED_EXTENSIONS:
        raise ValidationError("Неподдерживаемое расширение файла")
    if get_audio_duration(audio_file) > time_left:
        raise ValidationError(error_message)


def validate_youtube_url(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    if value:
        if not re.match(youtube_regex, value):
            raise ValidationError('Введите корректную ссылку на ютуб')
