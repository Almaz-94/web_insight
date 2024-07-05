import asyncio
import os

import django
from django.conf import settings
from nats.aio.client import Client as NATS


async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")


async def receive_message():
    nc = NATS()

    await nc.connect(servers=["nats://194.87.79.10:4222"])

    await nc.subscribe("web.wait.django", cb=message_handler)
    await nc.subscribe("web.wait.django.summary", cb=message_handler)
    print("Listening for messages...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

    await nc.drain()
    await nc.close()


if __name__ == '__main__':
    import django

    # Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Инициализируем Django
    django.setup()

    # Теперь можно импортировать модели и работать с ними
    from main.models import Summary


    # Пример использования ORM
    def print_all_my_models():
        objects = Summary.objects.all()
        for obj in objects:
            print(obj.user)

    print_all_my_models()
