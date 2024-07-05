import asyncio
from contextlib import asynccontextmanager

from faststream import FastStream, ContextRepo
from faststream.nats import NatsBroker

from main.nats_listener.routers import nats_route


@asynccontextmanager
async def lifespan(context: ContextRepo):
    # db = db

    context.set_global("model", "model")
    # context.set_global("model", db)

    yield
    print('end')


async def main():
    broker = NatsBroker(servers='nats://194.87.79.10:4222', )
    broker.include_router(nats_route)
    app = FastStream(broker, lifespan=lifespan)
    await app.run()


def run_nats_listener():
    asyncio.run(main())


if __name__ == "__main__":
    run_nats_listener()
