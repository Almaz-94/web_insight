import asyncio
import json

import nats
from nats.aio.msg import Msg
from pydantic import ValidationError
from django.conf import settings

from main.utils.message_entities import IncomeTranscribedText


def listen(server, queue):
    """
    Decorator
    Args:
        server: server_url
        queue:

    Returns:

    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nc = await nats.connect(server)

            async def cb(msg):
                nonlocal future
                try:
                    # Проверяем, завершен ли текущий future перед использованием
                    if future.done():
                        future = asyncio.Future()  # Создаем новый future, если текущий завершен

                    # Вызываем декорируемую функцию с полученным сообщением
                    result = await func(msg, *args, **kwargs)
                    if not future.done():
                        future.set_result(result)  # Устанавливаем результат для Future
                except Exception as e:
                    if not future.done():
                        future.set_exception(e)  # Устанавливаем исключение, если что-то пошло не так

            future = asyncio.Future()  # Создаем объект Future для контроля завершения
            await nc.subscribe(queue, cb=cb)
            await nc.flush()
            print("Listening for results...")

            return await future  # Ожидаем, пока Future не будет установлен и возвращаем результат

        return wrapper

    return decorator


@listen(server=settings.NATS_SERVER_URL, queue=f"{settings.QUEUE}")
async def received_transcribed_id(msg: Msg):
    try:
        # Преобразуем входную строку JSON с одинарными кавычками в правильный формат с двойными кавычками
        raw_data = msg.data.decode()
        print(f"Received raw data: {raw_data}")

        # Попробуем обработать данные как правильный JSON
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            # Если ошибка, заменим одинарные кавычки на двойные и попробуем снова
            corrected_data = raw_data.replace("'", '"')
            data = json.loads(corrected_data)

        a = IncomeTranscribedText(**data)
        print(f"Parsed data: {a}")
        print(a.tex_id)
        return int(a.tex_id)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None


@listen(server=settings.NATS_SERVER_URL, queue=f"{settings.QUEUE}")
async def received_summary_id(msg: Msg):
    print(f"Received result: {msg.data.decode()}")
    a = IncomeTranscribedText.parse_raw(msg.data)
    # if int(a.id_text)>0:
    #     #answer[id_text) = 'SELECT TEXT WHERE id = id_text'
    #     #send message answer[id_text)
    # Отправить сообщение с тем что переволд закончени и фильтр на хэгдлер что перевод закончкен ( не запустаться при нескольких запросах )
    return int(a.id_text)


if __name__ == '__main__':
    asyncio.run(received_transcribed_id())
