import re
from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    if value:
        if not re.match(youtube_regex, value):
            raise ValidationError('Invalid YouTube URL')