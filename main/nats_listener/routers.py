import json
import os

import django

from main.nats_listener.model import ListenTriggerMessage

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import logging

from asgiref.sync import sync_to_async
from faststream import Context
from faststream.nats import NatsRouter

from config_data.configs import settings as project_settings
from main.models import Summary
from main.utils.get_data import get_transcribed_text, get_summary_text

nats_server = project_settings.nats_listener.nats_server_url
nats_queue = project_settings.nats_listener.nats_queue
nats_route = NatsRouter(prefix='')


@nats_route.subscriber(subject=f'{nats_queue}.transcribe')
async def process_transcribed_text(msg, context=Context()):
    # db = context.db
    # raw_data = msg.data.decode()
    # try:
    #     data = json.loads(raw_data)
    # except json.JSONDecodeError:
    #     # Если ошибка, заменим одинарные кавычки на двойные и попробуем снова
    #     corrected_data = raw_data.replace("'", '"')
    #     data = json.loads(corrected_data)
    if type(msg) == bytes:
        print(f'Bytes: {msg}')
        return
    text_id = msg.get('tex_id')
    unique_id = msg.get('unique_id')
    logging.info(f"GET id {text_id}")
    text = await get_transcribed_text(text_id=text_id)
    logging.info(f"Received text: {text}")
    try:
        summary = await sync_to_async(Summary.objects.get)(unique_id=unique_id)
        summary.transcription = text
        summary.transcription_is_ready = True
        await sync_to_async(summary.save)()
    except Summary.DoesNotExist:
        logging.error(f'Summary with text_id {text_id} does not exist')
    print(text)
    # income_data = ListenTriggerMessage(**data)
    # print(f"Parsed data: {income_data}")
    # return income_data


@nats_route.subscriber(subject=f'{nats_queue}.summary')
async def process_summary_text(msg):
    if type(msg) == bytes:
        print(f'Bytes: {msg}')
        return
    text_id = msg['tex_id']
    unique_id = msg.get('unique_id')
    logging.info(f"GET id {text_id}")
    text = await get_summary_text(text_id=text_id)
    logging.info(f"Received text: {text}")
    try:
        summary = await sync_to_async(Summary.objects.get)(unique_id=unique_id)
        summary.summary = text
        summary.summary_is_ready = True
        await sync_to_async(summary.save)()
    except Summary.DoesNotExist:
        logging.error(f'Summary with text_id {text_id} does not exist')
    print(text)


@nats_route.subscriber(subject=f'{nats_queue}.test')
async def process_test(msg):
    if isinstance(msg, dict):
        # Если `msg` уже является словарем (dict), это означает, что данные уже декодированы
        data = msg
    else:
        # В противном случае, предполагаем, что `msg` является строкой и пытаемся её декодировать
        try:
            data = json.loads(msg)
        except json.JSONDecodeError:
            # Если не удалось декодировать, можно выполнить другие обработки по необходимости
            # Например, заменить одинарные кавычки на двойные и попробовать снова
            corrected_data = msg.replace("'", '"')
            data = json.loads(corrected_data)
        income_data = ListenTriggerMessage(**data)
        print(income_data)

    # Теперь можно обращаться к полям данных напрямую
    print(f"Received data: {data}")
