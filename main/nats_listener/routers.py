import logging

from faststream import Context
from faststream.nats import NatsRouter

from config_data.configs import settings
from main.utils.get_data import get_transcribed_text, get_summary_text

nats_server = settings.nats_listener.nats_server_url
nats_queue = settings.nats_listener.nats_queue
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
    logging.info(f"GET id {text_id}")
    text = await get_transcribed_text(text_id=text_id)
    logging.info(f"Received text: {text}")
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
    logging.info(f"GET id {text_id}")
    text = await get_summary_text(text_id=text_id)
    logging.info(f"Received text: {text}")
    print(text)
