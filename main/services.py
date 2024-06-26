import re
from tempfile import NamedTemporaryFile

import ffmpeg
import isodate
import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from main.s3 import S3Client


def get_s3_client():
    return S3Client(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
        bucket_name=settings.S3_BUCKET_NAME,
    )


def get_user_time(user):
    if user and user.is_authenticated:
        time_left = user.time_left
        error_message = f"Видео превышает по длине Ваше доступное время ({time_left} минута)"
    else:
        time_left = settings.ALLOWED_TIME_UNAUTH_USER
        error_message = f"Неавторизованные пользователи могут загружать видео продолжительностью " \
                        f"не более {time_left} минут"
    return time_left, error_message


def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.match(pattern, url)
    if match:
        return match.group(1)


def get_youtube_video_duration(youtube_link) -> int:
    video_id = extract_video_id(youtube_link)
    api_key = settings.YOUTUBE_API_KEY
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=contentDetails&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            duration = data['items'][0]['contentDetails']['duration']
            duration_minutes = isodate.parse_duration(duration).total_seconds() / 60
            return duration_minutes
    raise ValidationError("Что то пошло не так")


def get_audio_duration(file):
    with NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR) as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.flush()
        temp_file_path = temp_file.name
    try:
        probe = ffmpeg.probe(temp_file_path)
        duration = float(probe['format']['duration']) // 60  # minutes
    except ffmpeg.Error:
        raise ValidationError("Что то пошло не так")
    return duration


#
# async def get_media_duration_in_seconds(filepath):
#     """
#     Извлекает длину медиафайла (видео или аудио) из метаданных и возвращает её в секундах.
#
#     Args:
#         filepath: Путь к медиафайлу.
#
#     Returns:
#         Длительность медиафайла в секундах.
#     """
#     probe = await asyncio.to_thread(ffmpeg.probe, filepath)
#     format_info = probe["format"]
#     duration_sec = float(format_info["duration"])
#
#     print(f"Длина медиафайла: {duration_sec:.2f} секунд(ы)")
#     return duration_sec

def get_media_duration_in_seconds(filepath):
    """
    Извлекает длину медиафайла (видео или аудио) из метаданных и возвращает её в секундах.

    Args:
        filepath: Путь к медиафайлу.

    Returns:
        Длительность медиафайла в секундах.
    """
    print(f'FFMPEG {filepath}')
    probe = ffmpeg.probe(filepath)
    format_info = probe["format"]
    duration_sec = float(format_info["duration"])

    print(f"Длина медиафайла: {duration_sec:.2f} секунд(ы)")
    return duration_sec


def get_all_assistants():
    host = settings.API_HOST_URL
    response = requests.get(f'{host}/development/assistant/get_all').json()
    assistants = [(str(elem['id']), elem['name']) for elem in response]
    return tuple(assistants)
