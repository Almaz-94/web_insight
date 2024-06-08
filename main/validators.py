import re

from django.core.exceptions import ValidationError

from main.services import get_audio_duration, get_youtube_video_duration


def validate_audio_duration(file, time_left):
    duration_minutes = get_audio_duration(file)
    if duration_minutes:
        return duration_minutes <= time_left
    return False


def validate_youtube_duration(youtube_link, time_left):
    duration_minutes = get_youtube_video_duration(youtube_link)
    if duration_minutes:
        return duration_minutes <= time_left
    return False


def validate_youtube_url(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    if value:
        if not re.match(youtube_regex, value):
            raise ValidationError('Введите корректную ссылку на ютуб')
