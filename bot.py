import os

import disnake
from disnake.ext import commands, tasks
from loguru import logger


class Bot(commands.InteractionBot):
    """My BOt"""

    def __init__(self):
        super().__init__(
            intents=disnake.Intents.all()
        )
        self.update_description.start()
        self._once = True

    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")

        if self._once:
            self._once = False

    @tasks.loop(seconds=10)
    async def update_description(self):
        if self.is_ready():
            activity = disnake.Activity(
                name=f"{len(self.guilds)} servers", type=disnake.ActivityType.listening
            )
            status = disnake.Status.online
            await self.change_presence(activity=activity, status=status)
