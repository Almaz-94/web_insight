import asyncio
import os
from contextlib import asynccontextmanager

import django
from faststream import FastStream, ContextRepo
from faststream.nats import NatsBroker

from main.nats_listener.routers import nats_route


@asynccontextmanager
async def lifespan(context: ContextRepo):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    from main.models import Summary
    summary_model: Summary = Summary()

    context.set_global("summary_model", summary_model)
    # context.set_global("model", db)
    yield


async def main():
    broker = NatsBroker(servers='nats://194.87.79.10:4222', )
    broker.include_router(nats_route)
    app = FastStream(broker, lifespan=lifespan)
    await app.run()


def run_nats_listener():
    asyncio.run(main())


if __name__ == "__main__":
    run_nats_listener()
