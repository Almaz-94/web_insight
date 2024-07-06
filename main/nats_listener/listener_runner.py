import asyncio
import os
from contextlib import asynccontextmanager

import django
from faststream import FastStream, ContextRepo
from faststream.nats import NatsBroker

from config_data.configs import load_config
from main.nats_listener.routers import nats_route

settings = load_config('.env')


@asynccontextmanager
async def lifespan(context: ContextRepo):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    from main.models import Summary

    summary_model: Summary = Summary()

    context.set_global("summary_model", summary_model)
    yield


async def main():
    broker = NatsBroker(servers=settings.nats_listener.nats_server_url)
    broker.include_router(nats_route)
    app = FastStream(broker, lifespan=lifespan)
    await app.run()


def run_nats_listener():
    asyncio.run(main())


if __name__ == "__main__":
    run_nats_listener()
