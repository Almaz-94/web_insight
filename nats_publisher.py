import asyncio
import json

from nats.aio.client import Client as NATS


async def send_message():
    nc = NATS()

    await nc.connect(servers=["nats://194.87.79.10:4222"])
    message_data = {
        "unique_id": "47",
        "type": 'web',
        "tex_id": 87,
        "user_id": 3,
    }
    json_payload = json.dumps(message_data).encode('utf-8')

    # await nc.publish("web.wait.django.transcribe", b'Hello, NATS!')
    await nc.publish("web.wait.django.summary", json_payload)
    print("Message sent!")

    await nc.drain()
    await nc.close()


async def main():
    await send_message()


if __name__ == '__main__':
    asyncio.run(main())
