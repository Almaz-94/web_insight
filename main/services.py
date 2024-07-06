import re
from tempfile import NamedTemporaryFile

import aiohttp
import ffmpeg
import isodate
import requests
from aiohttp import ClientResponseError
from django.core.exceptions import ValidationError
from requests import RequestException

from django.conf import settings as django_settings

from config_data.configs import load_config
from main.s3 import S3Client

settings = load_config('.env')


def get_s3_client():
    return S3Client(
        access_key=settings.s3_config.access_key,
        secret_key=settings.s3_config.secret_key,
        endpoint_url=settings.s3_config.endpoint_url,
        bucket_name=settings.s3_config.bucket_name,
    )


def get_user_time(user):
    if user and user.is_authenticated:
        time_left = user.time_left
        error_message = f"Видео превышает по длине Ваше доступное время ({time_left} мин)"
    else:
        time_left = django_settings.ALLOWED_TIME_UNAUTH_USER
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
    api_key = settings.youtube_api.youtube_api_key
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
    host = settings.api_config.api_host_url
    url = f'{host}{settings.api_config.get_all_assistant}'
    response = requests.get(url).json()
    assistants = [(str(elem['assistant_id']), elem['name']) for elem in response]
    return tuple(assistants)


async def start_task_from_youtube(summary):
    host = settings.api_config.api_host_url
    endpoint = settings.api_config.start_youtube_process
    url = host + endpoint
    data = {
        "unique_id": "unique_id",
        "user_id": summary.user.id if summary.user else summary.session_key,
        "youtube_url": summary.youtube_link,
        "assistant_id": int(summary.script),
        "publisher_queue": settings.nats_listener.nats_queue,
        "source": "web",
        "user_prompt": summary.prompt,
        "description": "string"
    }
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
    except aiohttp.ClientError as e:
        print(f'Error sending data: {e}')


async def start_task_from_storage(object):
    host = settings.api_config.api_host_url
    endpoint = settings.api_config.start_s3_process
    url = host + endpoint
    data = {
        "user_id": object.user.id if object.user else object.session_key,
        "s3_path": object.file_link_s3,
        "assistant_id": object.script,
        "publisher_queue": settings.nats_listener.nats_queue,
        "storage_url": object.file_link_s3,
        "source": "web",
        "user_prompt": object.prompt,
        "description": "string"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                response.raise_for_status()

    except RequestException as e:
        print(f'Ошибка отправки данных {e}')
    except ClientResponseError as e:
        print(f'ClientResponseError: {e.status}, message={e.message}, url={e.request_info.url}')
    except aiohttp.ClientError as e:
        print(f'aiohttp.ClientError: {e}')
    except Exception as e:
        print(f'Error sending data: {e}')
