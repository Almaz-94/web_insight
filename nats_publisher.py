import asyncio

import nats_client
from nats.aio.client import Client as NATS


async def send_message():
    nc = NATS()

    await nc.connect(servers=["nats://194.87.79.10:4222"])

    # await nc.publish("web.wait.django", b'Hello, NATS!')
    await nc.publish("web.wait.django.summary", b'Hello, nats summary')
    print("Message sent!")

    await nc.drain()
    await nc.close()


async def main():
    await send_message()


if __name__ == '__main__':
    asyncio.run(main())
