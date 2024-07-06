import json
import os

import django
from asgiref.sync import sync_to_async  # Импортируем sync_to_async для работы с асинхронными вызовами в Django
from faststream import Context
from faststream.nats import NatsRouter

from config_data.configs import settings
from main.nats_listener.model import ListenTriggerMessage
from main.utils.get_data import get_summary_text

nats_server = settings.nats_listener.nats_server_url
nats_queue = settings.nats_listener.nats_queue
nats_route = NatsRouter(prefix='')


@nats_route.subscriber(subject=f'{nats_queue}.transcribe')
async def process_transcribed_text(msg, context=Context()):
    summary_model = context.summary_model

    @sync_to_async
    def save_transcribe_text(summary_model, id, text):
        summary_obj, created = summary_model.objects.get_or_create(unique_id=id)
        summary_obj.transcription = text
        summary_obj.save()

    @sync_to_async
    def print_transcribed():
        summaries = summary_model.objects.all()
        print(summaries)

    await print_transcribed()
    # raw_data = msg.data.decode()
    # try:
    #     data = json.loads(raw_data)
    # except json.JSONDecodeError:
    #     # Если ошибка, заменим одинарные кавычки на двойные и попробуем снова
    #     corrected_data = raw_data.replace("'", '"')
    #     data = json.loads(corrected_data)
    # income_data = ListenTriggerMessage(**data)
    # text = await get_transcribed_text(text_id=income_data.tex_id)
    # save_transcribe_text(summary_model, income_data.unique_id, text)
    # # database.save(income_data.unique_id)
    # print(f"Parsed data: {income_data}")
    # return income_data


@nats_route.subscriber(subject=f'{nats_queue}.summary')
async def process_summary_text(msg):
    raw_data = msg.data.decode()
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        # Если ошибка, заменим одинарные кавычки на двойные и попробуем снова
        corrected_data = raw_data.replace("'", '"')
        data = json.loads(corrected_data)
    income_data = ListenTriggerMessage(**data)
    text = await get_summary_text(text_id=income_data.tex_id)
    print(text)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    from main.models import Summary

    summary = Summary.objects.all()
    print(summary)
