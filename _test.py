import asyncio

from main.utils.get_data import get_summary_text


async def main():
    await get_summary_text(12)


if __name__ == '__main__':
    asyncio.run(main())
