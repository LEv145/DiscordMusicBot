import asyncio

from bot import Bot


async def main():
    bot = Bot()
    bot.run()


asyncio.run(main())
