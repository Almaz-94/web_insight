import json
import logging
import os

import django
from asgiref.sync import sync_to_async  # Импортируем sync_to_async для работы с асинхронными вызовами в Django
from faststream import Context
from faststream.nats import NatsRouter

from config_data.configs import settings
from main.nats_listener.model import ListenTriggerMessage
from main.utils.get_data import get_transcribed_text, get_summary_text

nats_server = settings.nats_listener.nats_server_url
nats_queue = settings.nats_listener.nats_queue
nats_route = NatsRouter(prefix='')


@nats_route.subscriber(subject=f'{nats_queue}.transcribe')
async def process_transcribed_text(msg, context=Context()):
    summary_model = context.summary_model

    @sync_to_async
    def save_transcribe_text(model, unique_id, text):
        summary_obj, created = model.objects.get_or_create(unique_id=unique_id)
        summary_obj.transcription = text
        summary_obj.transcription_is_ready = True
        summary_obj.save()

    if isinstance(msg, dict):
        # Если `msg` уже является словарем (dict), это означает, что данные уже декодированы
        data = msg
    else:
        # В противном случае, предполагаем, что `msg` является строкой и пытаемся её декодировать
        try:
            data = json.loads(msg)
        except json.JSONDecodeError:
            corrected_data = msg.replace("'", '"')
            data = json.loads(corrected_data)
    income_data = ListenTriggerMessage(**data)

    transcribed_text = await get_transcribed_text(text_id=income_data.tex_id)
    await save_transcribe_text(summary_model, income_data.unique_id, transcribed_text)


@nats_route.subscriber(subject=f'{nats_queue}.summary')
async def process_summary_text(msg, context=Context()):
    summary_model = context.summary_model

    @sync_to_async
    def save_summary_text(model, unique_id, text):
        summary_obj, created = model.objects.get_or_create(unique_id=unique_id)
        summary_obj.summary = text
        summary_obj.summary_is_ready = True
        summary_obj.save()

    if isinstance(msg, dict):
        # Если `msg` уже является словарем (dict), это означает, что данные уже декодированы
        data = msg
    else:
        # В противном случае, предполагаем, что `msg` является строкой и пытаемся её декодировать
        try:
            data = json.loads(msg)
        except json.JSONDecodeError:
            corrected_data = msg.replace("'", '"')
            data = json.loads(corrected_data)

    income_data = ListenTriggerMessage(**data)
    summary_text = await get_summary_text(text_id=income_data.tex_id)
    await save_summary_text(summary_model, income_data.unique_id, summary_text)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    from main.models import Summary

    summary = Summary.objects.all()
    print(summary)
