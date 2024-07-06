import uuid

from django.conf import settings
from django.db import models

from main.validators import validate_youtube_url

NULLABLE = {'blank': True, 'null': True}


def generate_uuid():
    return str(uuid.uuid4())


class Summary(models.Model):
    unique_id = models.CharField(max_length=100, unique=True, default=generate_uuid)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    session_key = models.CharField(max_length=40, verbose_name='сессия', **NULLABLE)
    youtube_link = models.CharField(max_length=100, verbose_name='Youtube ссылка',
                                    validators=[validate_youtube_url], **NULLABLE)
    audio_file = models.FileField(upload_to='audio_files/', verbose_name='аудио файл', **NULLABLE)
    file_link_s3 = models.TextField(verbose_name='ссылка на файл в s3', **NULLABLE)
    transcription = models.TextField(verbose_name='транскрибация', **NULLABLE)
    summary = models.TextField(verbose_name='саммари', **NULLABLE)
    transcription_is_ready = models.BooleanField(default=False, verbose_name="транскрибация готова")
    summary_is_ready = models.BooleanField(default=False, verbose_name="саммари готов")
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время запроса')
    script = models.CharField(max_length=40, verbose_name='сценарий обработки')
    prompt = models.TextField(verbose_name='Промт пользователя', **NULLABLE)

    # def __str__(self):
    #     return f'{self.audio_file}, {self.file_link_s3}'

    class Meta:
        verbose_name = 'запрос к воркеру'
        verbose_name_plural = 'запросы к воркеру'


class SummariesAndTranscriptions(models.Model):
    transcription = models.TextField(verbose_name='транскрибация', **NULLABLE)
    summary = models.TextField(verbose_name='саммари', **NULLABLE)

    def __str__(self):
        return f'Summary and Transcription: {self.id}'

    class Meta:
        verbose_name = 'саммари и транскрибация'
        verbose_name_plural = 'саммари и транскрибации'


class YoutubeRequest(models.Model):
    unique_id = models.CharField(max_length=100, unique=True, default=generate_uuid)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    session_key = models.CharField(max_length=40, verbose_name='сессия', **NULLABLE)
    youtube_link = models.CharField(max_length=100, verbose_name='Youtube ссылка', validators=[validate_youtube_url], **NULLABLE)
    summary_and_transcriptions = models.ForeignKey(SummariesAndTranscriptions, on_delete=models.SET_NULL, **NULLABLE)
    transcription_is_ready = models.BooleanField(default=False, verbose_name="транскрибация готова")
    summary_is_ready = models.BooleanField(default=False, verbose_name="саммари готов")
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время запроса')
    script = models.CharField(max_length=40, verbose_name='сценарий обработки')
    prompt = models.TextField(verbose_name='Промт пользователя', **NULLABLE)

    def __str__(self):
        return f'YoutubeRequest: {self.unique_id}'

    class Meta:
        verbose_name = 'запрос к воркеру'
        verbose_name_plural = 'запросы к воркеру'


class S3Request(models.Model):
    unique_id = models.CharField(max_length=100, unique=True, default=generate_uuid)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    session_key = models.CharField(max_length=40, verbose_name='сессия', **NULLABLE)
    audio_file = models.FileField(upload_to='audio_files/', verbose_name='аудио файл', **NULLABLE)
    file_link_s3 = models.TextField(verbose_name='ссылка на файл в s3', **NULLABLE)
    summary_and_transcriptions = models.ForeignKey(SummariesAndTranscriptions, on_delete=models.SET_NULL, **NULLABLE)
    transcription_is_ready = models.BooleanField(default=False, verbose_name="транскрибация готова")
    summary_is_ready = models.BooleanField(default=False, verbose_name="саммари готов")
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата и время запроса')
    script = models.CharField(max_length=40, verbose_name='сценарий обработки')
    prompt = models.TextField(verbose_name='Промт пользователя', **NULLABLE)

    def __str__(self):
        return f'S3Request: {self.unique_id}'

    class Meta:
        verbose_name = 's3 запрос'
        verbose_name_plural = 's3 запросы'
